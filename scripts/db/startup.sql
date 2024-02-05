create sequence spp_plugins_meta_id_seq
    as integer;

create table if not exists spp_source
(
    source_id serial
        primary key,
    name      text                     not null
        unique,
    config    json,
    sphere    text,
    load_date timestamp with time zone not null
);

create table if not exists spp_document
(
    doc_id     serial
        primary key,
    title      text                     not null,
    abstract   text,
    text       text,
    web_link   text                     not null,
    local_link text,
    other_data json,
    pub_date   timestamp with time zone not null,
    load_date  timestamp with time zone,
    source_id  integer                  not null
        references spp_source
);

create table if not exists spp_task_status
(
    status_id serial
        constraint spp_task_status_pk
            primary key,
    name      text    not null,
    code      integer not null
);

comment on table spp_task_status is 'таблица возможных статусов состояний';

create table if not exists spp_plugin_type
(
    id   serial
        constraint spp_plugin_type_pk
            primary key,
    type text not null
);

create table if not exists spp_model
(
    id       serial
        constraint spp_model_pk
            primary key,
    name     text not null,
    comment  text,
    pub_date timestamp with time zone
);

create table if not exists spp_plugin
(
    plugin_id  serial
        primary key,
    repository text    not null,
    active     boolean,
    pub_date   timestamp with time zone,
    other_data json,
    source_id  integer
        references spp_source,
    type       integer
        constraint spp_plugin_spp_plugin_type_id_fk
            references spp_plugin_type,
    model_id   integer
        constraint spp_plugin_spp_model_id_fk
            references spp_model,
    constraint check_foreign_id
        check (((source_id IS NOT NULL) AND (model_id IS NULL) AND (type = 1)) OR
               ((source_id IS NULL) AND (model_id IS NOT NULL) AND (type = 2)))
);

comment on constraint check_foreign_id on spp_plugin is 'Check plugin type and correct foreign refference to source or model';

create table if not exists spp_task
(
    id               integer default nextval('spp_plugins_meta_id_seq'::regclass) not null
        constraint spp_task_pk
            primary key,
    time_next_launch timestamp with time zone,
    plugin_id        integer                                                      not null
        constraint spp_task_spp_plugin_plugin_id_fk
            references spp_plugin,
    last_finish_time timestamp with time zone,
    status_id        integer                                                      not null
        constraint spp_task_spp_task_status_status_id_fk
            references spp_task_status,
    error_stack      integer default 0                                            not null
);

comment on column spp_task.status_id is 'Статус работы плагина и его состояний';

alter sequence spp_plugins_meta_id_seq owned by spp_task.id;

create table if not exists task_error
(
    id      serial
        constraint task_error_pk
            primary key,
    text    text,
    data    timestamp with time zone not null,
    task_id integer                  not null
        constraint task_error___fk
            references spp_task
);

create table if not exists spp_model_score
(
    id          serial
        constraint spp_model_score_pk
            primary key,
    score       json,
    plugin_id   integer
        constraint spp_model_score_spp_plugin_plugin_id_fk
            references spp_plugin,
    document_id integer
        constraint spp_model_score_spp_document_doc_id_fk
            references spp_document
);

create table if not exists roles
(
    id      serial
        constraint roles_pk
            primary key,
    name    text,
    comment integer
);

create table if not exists spp_plugins_roles
(
    id        serial
        constraint spp_plugins_roles_pk
            primary key,
    plugin_id integer
        constraint spp_plugins_roles_spp_plugin_plugin_id_fk
            references spp_plugin,
    role_id   integer
        constraint spp_plugins_roles___fk
            references roles
);

create table if not exists spp_roles_sources
(
    id        serial
        constraint spp_roles_sources_pk
            primary key,
    role      integer
        constraint spp_roles_sources_roles_id_fk
            references roles,
    source_id integer
        constraint spp_roles_sources_spp_source_source_id_fk
            references spp_source
);

create or replace view "task dashboard"
            (sousrce, plugin, type, status, "old launch", "future launch 1", "task id", "status id") as
SELECT ss.name                   AS sousrce,
       sp.repository             AS plugin,
       sp.type,
       sts.name                  AS status,
       spp_task.last_finish_time AS "old launch",
       spp_task.time_next_launch AS "future launch 1",
       spp_task.id               AS "task id",
       spp_task.status_id        AS "status id"
FROM spp_plugin sp
         JOIN spp_task ON sp.plugin_id = spp_task.plugin_id
         JOIN spp_source ss ON ss.source_id = sp.source_id
         JOIN spp_task_status sts ON spp_task.status_id = sts.status_id;

create or replace view view_name
            (sousrce, plugin, type, status, "old launch", "future launch 1", "task id", "status id", active) as
SELECT ss.name                   AS sousrce,
       sp.repository             AS plugin,
       pt.type,
       sts.name                  AS status,
       spp_task.last_finish_time AS "old launch",
       spp_task.time_next_launch AS "future launch 1",
       spp_task.id               AS "task id",
       spp_task.status_id        AS "status id",
       sp.active
FROM spp_plugin sp
         JOIN spp_task ON sp.plugin_id = spp_task.plugin_id
         JOIN spp_source ss ON ss.source_id = sp.source_id
         JOIN spp_task_status sts ON spp_task.status_id = sts.status_id
         JOIN spp_plugin_type pt ON sp.type = pt.id;

create or replace function set_plugin_activity(__plugin_id integer, __activity boolean) returns void
    language plpgsql
as
$$
begin
    UPDATE public.spp_plugin as sp
    SET active = __activity
    WHERE public.spp_plugin.plugin_id = __plugin_id;
end;
$$;

create or replace function task_clear(__task_id integer) returns boolean
    language plpgsql
as
$$
begin
    IF (EXISTS(SELECT id FROM spp_task WHERE id = __task_id)) THEN
        RETURN FALSE;
    end if;

    DELETE
    FROM public.spp_task
    WHERE id = __task_id;
    return TRUE;
end;
$$;

create or replace function set_task_status(__plugin_id integer, __status_code integer) returns boolean
    language plpgsql
as
$$
declare
    __status_id integer;
begin


    SELECT status_id INTO __status_id FROM public.spp_task_status WHERE code = __status_code;

    UPDATE public.spp_task
    SET status_id = __status_id
    WHERE plugin_id = __plugin_id;
    return TRUE;
end;
$$;

create or replace function task_finish(__plugin_id integer, __restart_time interval) returns boolean
    language plpgsql
as
$$
declare
    __status_id            integer;
    __new_time_next_launch timestamp WITH TIME ZONE;
    __last_finish_time     timestamp WITH TIME ZONE;
begin


    SELECT status_id INTO __status_id FROM public.spp_task_status WHERE name LIKE 'FINISHED';
    SELECT now()::timestamp WITH TIME ZONE INTO __last_finish_time;


    IF (__restart_time IS NULL) THEN
        __restart_time := '7 days'::interval;
    end IF;

    __new_time_next_launch := __last_finish_time + __restart_time;
    UPDATE public.spp_task
        SET status_id        = __status_id,
            last_finish_time = __last_finish_time,
            time_next_launch = __new_time_next_launch
        WHERE plugin_id = __plugin_id;

    return TRUE;
end;
$$;

create or replace function equal_documents(doc_id_1 integer, title_1 text, web_link_1 text, pub_date_1 timestamp with time zone, source_id_1 integer, doc_id_2 integer, title_2 text, web_link_2 text, pub_date_2 timestamp with time zone, source_id_2 integer) returns boolean
    language plpgsql
as
$$

begin

    --     1. Сначала проверяем совпадают ли у документов источники
--     Если источники документов не равны, то ДОКУМЕНТЫ НЕ РАВНЫ
    IF (source_id_1 <> source_id_2) THEN
        RETURN FALSE;
    end if;

--      2. Проверяем есть ли у документов поле ID. Если у какого-нибудь документа поля ID нет, то проверять соответствие будем по 3 уникальным полям, который должны быть.
    IF (doc_id_1 IS NULL) OR (doc_id_2 IS NULL) THEN
        RETURN (title_1 = title_2) AND (web_link_1 = web_link_2) AND (pub_date_1 = pub_date_2);
    end if;

--      3. Если у двух документов есть ID, то сравнение происходит по ним
    IF (doc_id_1 IS NOT NULL) AND (doc_id_2 IS NOT NULL) THEN
        RETURN doc_id_1 = doc_id_2;
    end if;

    RETURN FALSE;
end;
$$;

create or replace function create_task(__plugin_id integer, __time_next_launch timestamp with time zone, __status_code integer) returns integer
    language plpgsql
as
$$
declare
    __time           timestamp WITH TIME ZONE;
    __default_status integer;
    __status_id      integer;
begin
    IF (__time_next_launch IS NULL) THEN
        __time := now();
    ELSE
        __time := __time_next_launch;
    end if;

    IF (__status_code IS NULL) THEN
        __status_id := 1;
    ELSE
        SELECT status_id INTO __status_id FROM public.spp_task_status WHERE code = __status_code;
    end if;

    IF (EXISTS(SELECT id FROM public.spp_task WHERE plugin_id = __plugin_id)) THEN
        RAISE EXCEPTION 'Plugin with id % already processing', __plugin_id USING HINT = 'Please check your plugin id';
    end if;

    INSERT INTO public.spp_task (time_next_launch, plugin_id, status_id)
    VALUES (__time, __plugin_id, __status_id);

    RETURN currval('spp_plugins_meta_id_seq');
end;
$$;

create or replace function get_all_active_plugins()
    returns TABLE(plugin_id integer, repository text, active boolean, pub_date timestamp with time zone)
    language plpgsql
as
$$
begin
    return query select sp.plugin_id,
                        sp.repository,
                        sp.active,
                        sp.pub_date
--                         sp.other_data
                 from public.spp_plugin as sp
                 WHERE sp.active = TRUE;
end;
$$;

create or replace function get_all_documents_by_source(__source_id integer, __sourcename text)
    returns TABLE(doc_id integer, title text, abstract text, text text, web_link text, local_link text, other_data json, pub_date timestamp with time zone, load_date timestamp with time zone)
    language plpgsql
as
$$
declare
    temp_spource_id INTEGER;

begin
    IF (__source_id IS NULL) THEN
-- 		Если source_id пустой, то нужно найти источник по его имени
        SELECT s.source_id INTO temp_spource_id FROM public.safe_get_source(__sourcename) as s;
    ELSE
--      Если source_id есть, то просто вставляем его
        temp_spource_id := __source_id;
    END IF;

    return query select sd.doc_id,
                        sd.title,
                        sd.abstract,
                        sd.text,
                        sd.web_link,
                        sd.local_link,
                        sd.other_data,
                        sd.pub_date,
                        sd.load_date
                 from public.spp_document as sd
                 WHERE sd.source_id = temp_spource_id;
end;
$$;

create or replace function relevant_plugins_for_processing()
    returns TABLE(plugin_id integer, repository text, pub_date timestamp with time zone, other_data json)
    language plpgsql
as
$$
begin
    --   Релевантные задачи для исполнения на платформе это те:
--         1. Плагин является активным
--         2. связанная задача или не существует
--         3. связанная задача в состоянии FINISHED или BROKEN и время старта < now()
--

    RETURN QUERY SELECT sp.plugin_id  as plugin_id,
                        sp.repository as repository,
                        sp.pub_date   as pub_date,
                        sp.other_data as other_data
                 FROM public.spp_task as st
                          RIGHT JOIN public.spp_plugin sp on sp.plugin_id = st.plugin_id
                 WHERE sp.active IS TRUE
                   AND (
                         st.plugin_id IS NULL
                         OR
                         (st.plugin_id IS NOT NULL
                             AND
                          (st.status_id = 7 OR st.status_id = 8 or st.status_id = 9) AND st.time_next_launch < now()
                             )
                     );

end;
$$;

create or replace function safe_get_source(__sourcename text)
    returns TABLE(source_id integer, sourcename text, config json, sphere text, load_date timestamp with time zone)
    language plpgsql
as
$$
declare
    d_check integer;
begin
    IF EXISTS (select * from public.spp_source where name LIKE __sourcename) THEN
        return query select * from public.spp_source where name LIKE __sourcename;
    ELSE
        INSERT INTO public.spp_source(source_id, name, load_date) values (default, __sourcename, NOW());
        return query select s.source_id, s.name, s.config, s.sphere, s.load_date
                     from public.spp_source as s
                     where name LIKE __sourcename;
    END IF;
end;
$$;

create or replace function safe_init_document(__source_id integer, __sourcename text, __title text, __abstract text, __web_link text, __pub_date timestamp with time zone) returns boolean
    language plpgsql
as
$$
declare
    temp_spource_id INTEGER;

begin
    IF (__source_id IS NULL) THEN
-- 		Если source_id пустой, то нужно найти источник по его имени
        SELECT s.source_id INTO temp_spource_id FROM public.safe_get_source(__sourcename) as s;
    ELSE
--      Если source_id есть, то просто вставляем его
        temp_spource_id := __source_id;
    END IF;

    if not EXISTS(select *
                  FROM public.spp_document
                  WHERE source_id = temp_spource_id
                    AND title = __title
                    AND abstract = __abstract)
    THEN

        insert into public.spp_document (title, abstract, web_link, pub_date, source_id)
        VALUES (__title, __abstract, __web_link, __pub_date, temp_spource_id);

        return true;
    else
        return false;
    end if;
end;
$$;

create or replace function safe_update_document(__source_id integer, __sourcename text, __doc_id integer, __title text, __abstract text, __text text, __web_link text, __local_link text, __other_data json, __pub_date timestamp with time zone, __load_date timestamp with time zone) returns boolean
    language plpgsql
as
$$
declare
    temp_spource_id INTEGER;

begin
    IF (__source_id IS NULL) THEN
-- 		Если source_id пустой, то нужно найти источник по его имени
        SELECT s.source_id INTO temp_spource_id FROM public.safe_get_source(__sourcename) as s;
    ELSE
--      Если source_id есть, то просто вставляем его
        temp_spource_id := __source_id;
    END IF;

--     Если документ существует и обновился, то возвращаем TRUE
    IF (SELECT *
        FROM public.update_document(
                __source_id,
                __sourcename,
                __doc_id,
                __title,
                __abstract,
                __text,
                __web_link,
                __local_link,
                __other_data,
                __pub_date,
                __load_date
            ))::boolean IS TRUE THEN
        RETURN TRUE;
    ELSE
--         Если документа не существовало, то добавляем его и возвращаем TRUE
        INSERT INTO public.spp_document (title, abstract, text, web_link, local_link, other_data, pub_date, load_date,
                                         source_id)
        VALUES (__title,
                __abstract,
                __text,
                __web_link,
                __local_link,
                __other_data,
                __pub_date,
                __load_date,
                temp_spource_id);

        RETURN FALSE;
    END IF;

end;
$$;

create or replace function set_next_launch_time(__task_id integer, __next_time timestamp with time zone) returns boolean
    language plpgsql
as
$$
begin
    IF (EXISTS(SELECT id FROM spp_task WHERE id = __task_id)) THEN
        RETURN FALSE;
    end if;

    UPDATE public.spp_task
    SET time_next_launch = __next_time
    WHERE id = __task_id;
    return TRUE;
end;
$$;

create or replace function set_plugin_pub_date(__plugin_id integer, __pub_date timestamp with time zone) returns void
    language plpgsql
as
$$
begin
    UPDATE public.spp_plugin as sp
    SET pub_date = __pub_date
    WHERE public.spp_plugin.plugin_id = __plugin_id;
end;
$$;

create or replace function update_document(__source_id integer, __sourcename text, __doc_id integer, __title text, __abstract text, __text text, __web_link text, __local_link text, __other_data json, __pub_date timestamp with time zone, __load_date timestamp with time zone) returns boolean
    language plpgsql
as
$$
declare
    temp_spource_id INTEGER;

begin
    IF (__source_id IS NULL) THEN
-- 		Если source_id пустой, то нужно найти источник по его имени
        SELECT s.source_id INTO temp_spource_id FROM public.safe_get_source(__sourcename) as s;
    ELSE
--      Если source_id есть, то просто вставляем его
        temp_spource_id := __source_id;
    END IF;


    IF exists(SELECT *
              FROM public.spp_document as sd
              WHERE public.equal_documents(
                            sd.doc_id,
                            sd.title,
                            sd.web_link,
                            sd.pub_date,
                            sd.source_id,
                            __doc_id,
                            __title,
                            __web_link,
                            __pub_date,
                            temp_spource_id
                        )) THEN

        UPDATE "sourceParserPlatform".public.spp_document as sd
        SET title      = __title,
            abstract   = __abstract,
            text       = __text,
            web_link   = __web_link,
            local_link = __local_link,
            other_data = __other_data,
            pub_date   = __pub_date,
            load_date  = __load_date
        WHERE public.equal_documents(
                      sd.doc_id,
                      sd.title,
                      sd.web_link,
                      sd.pub_date,
                      sd.source_id,
                      __doc_id,
                      __title,
                      __web_link,
                      __pub_date,
                      temp_spource_id);

        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;

end;
$$;

create or replace function task_broke(__plugin_id integer) returns boolean
    language plpgsql
as
$$
--     Функция вызывается, когда задача уходит в отбраковку.
--     При падении задачи в ошибку, SPP пытается перезапустить ее через N минут.
--     Если после 3 перезапусков подряд, задача снова упадет в ошибку - Она уходит надолго
--     Временно работает простая обработка ошибок
--     Параметр рестарта и текста ошибки - временно не используется
declare
    __status_id            integer;
    __error_stack          integer;
    __restart_error_time   interval;
    __restart_stack_time   interval;
    __new_stack            integer;
    __new_time_next_launch timestamp WITH TIME ZONE;
    __last_finish_time     timestamp WITH TIME ZONE;
begin


    SELECT status_id INTO __status_id FROM public.spp_task_status WHERE name LIKE 'BROKEN';
    SELECT now()::timestamp WITH TIME ZONE INTO __last_finish_time;
    SELECT '1 day'::interval INTO __restart_error_time;
    SELECT '10 minutes'::interval INTO __restart_stack_time;
    SELECT task.error_stack INTO __error_stack FROM public.spp_task as task WHERE task.plugin_id = __plugin_id;

    IF (__error_stack >= 3) THEN
--         Число попыток перезапуска превысило 3. Нужно отправлять на исправления
        __new_time_next_launch := __last_finish_time + __restart_error_time;
        __new_stack := 0;
    ELSE
        __new_time_next_launch := __last_finish_time + __restart_stack_time;
        __new_stack := __error_stack + 1;
    end IF;

    UPDATE public.spp_task as task
    SET status_id        = __status_id,
        last_finish_time = __last_finish_time,
        time_next_launch = __new_time_next_launch,
        error_stack = __new_stack
    WHERE task.plugin_id = __plugin_id;

    return TRUE;
end;
$$;

create or replace function get_all_documents_for_hash_by_source(__source_id integer, __sourcename text)
    returns TABLE(doc_id integer, title text, web_link text, pub_date timestamp with time zone)
    language plpgsql
as
$$
declare
    temp_spource_id INTEGER;

begin
    IF (__source_id IS NULL) THEN
-- 		Если source_id пустой, то нужно найти источник по его имени
        SELECT s.source_id INTO temp_spource_id FROM public.safe_get_source(__sourcename) as s;
    ELSE
--      Если source_id есть, то просто вставляем его
        temp_spource_id := __source_id;
    END IF;

    return query select sd.doc_id,
                        sd.title,
                        sd.web_link,
                        sd.pub_date
                 from public.spp_document as sd
                 WHERE sd.source_id = temp_spource_id;
end;
$$;

create or replace function relevant_plugin_for_processing(__plugin_type text)
    returns TABLE(plugin_id integer, repository text, pub_date timestamp with time zone, type text)
    language plpgsql
as
$$
declare
    __plugin_type_id INTEGER;
begin
--   Релевантный плагин для исполнения на платформе это тот:
--         1. Плагин является активным
--         2. связанная задача или не существует
--         3. связанная задача в состоянии (FINISHED или BROKEN или TERMINATED) и время старта < now()
--
    IF (__PLUGIN_TYPE IS NULL or __PLUGIN_TYPE like 'ALL') THEN
-- 		Если __PLUGIN_TYPE пустой, то мы не должны обращать внимания на группу
        __plugin_type_id := 0;
    ELSE
        SELECT pl_type.id INTO __plugin_type_id FROM public.spp_plugin_type as pl_type WHERE pl_type.type = __PLUGIN_TYPE LIMIT 1;
    END IF;

    RETURN QUERY SELECT sp.plugin_id  as plugin_id,
                        sp.repository as repository,
                        sp.pub_date   as pub_date,
                        spt.type as type
                 FROM public.spp_task as st
                    RIGHT JOIN public.spp_plugin sp on sp.plugin_id = st.plugin_id
                    RIGHT JOIN public.spp_plugin_type spt on spt.id = sp.type
                 WHERE sp.active IS TRUE
                   AND (
                         st.plugin_id IS NULL
                         OR
                         (st.plugin_id IS NOT NULL
                             AND
                          (st.status_id = 7 OR st.status_id = 8 or st.status_id = 9) AND st.time_next_launch < now()
                             )
                     )
                   AND (__PLUGIN_TYPE IS NULL
                            OR (__PLUGIN_TYPE IS NOT NULL AND __plugin_type_id = 0)
                            OR (__PLUGIN_TYPE IS NOT NULL AND sp.type = __plugin_type_id)
                       )
                LIMIT 1;

end;
$$;

