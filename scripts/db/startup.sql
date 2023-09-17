create sequence spp_plugins_meta_id_seq
    as integer;

create table if not exists spp_source
(
    source_id serial,
    name      text      not null,
    config    json,
    sphere    text,
    load_date timestamp not null,
    primary key (source_id),
    unique (name)
);

create table if not exists spp_document
(
    doc_id     serial,
    title      text      not null,
    abstract   text,
    text       text,
    web_link   text      not null,
    local_link text,
    other_data json,
    pub_date   timestamp not null,
    load_date  timestamp,
    source_id  integer   not null,
    primary key (doc_id),
    foreign key (source_id) references spp_source
);

create table if not exists spp_plugin
(
    plugin_id  serial,
    repository text    not null,
    active     boolean,
    pub_date   timestamp,
    other_data json,
    source_id  integer not null,
    primary key (plugin_id),
    foreign key (source_id) references spp_source
);

create table if not exists spp_task_status
(
    status_id serial,
    name      text    not null,
    code      integer not null,
    constraint spp_task_status_pk
        primary key (status_id)
);

comment on table spp_task_status is 'таблица возможных статусов состояний';

create table if not exists spp_task
(
    id               integer default nextval('spp_plugins_meta_id_seq'::regclass) not null,
    time_next_launch timestamp,
    plugin_id        integer                                                      not null,
    last_finish_time timestamp,
    status_id        integer                                                      not null,
    constraint spp_task_pk
        primary key (id),
    constraint spp_task_spp_plugin_plugin_id_fk
        foreign key (plugin_id) references spp_plugin,
    constraint spp_task_spp_task_status_status_id_fk
        foreign key (status_id) references spp_task_status
);

comment on column spp_task.status_id is 'Статус работы плагина и его состояний';

alter sequence spp_plugins_meta_id_seq owned by spp_task.id;

create or replace function safe_get_source(__sourcename text)
    returns TABLE
            (
                source_id  integer,
                sourcename text,
                config     json,
                sphere     text,
                load_date  timestamp without time zone
            )
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

create or replace function safe_init_document(__source_id integer, __sourcename text, __title text, __abstract text,
                                              __web_link text, __pub_date timestamp without time zone) returns boolean
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

create or replace function get_all_documents_by_source(__source_id integer, __sourcename text)
    returns TABLE
            (
                doc_id     integer,
                title      text,
                abstract   text,
                text       text,
                web_link   text,
                local_link text,
                other_data json,
                pub_date   timestamp without time zone,
                load_date  timestamp without time zone
            )
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

create or replace function safe_update_document(__source_id integer, __sourcename text, __doc_id integer, __title text,
                                                __abstract text, __text text, __web_link text, __local_link text,
                                                __other_data json, __pub_date timestamp without time zone,
                                                __load_date timestamp without time zone) returns boolean
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

create or replace function equal_documents(doc_id_1 integer, title_1 text, web_link_1 text,
                                           pub_date_1 timestamp without time zone, source_id_1 integer,
                                           doc_id_2 integer, title_2 text, web_link_2 text,
                                           pub_date_2 timestamp without time zone, source_id_2 integer) returns boolean
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

create or replace function update_document(__source_id integer, __sourcename text, __doc_id integer, __title text,
                                           __abstract text, __text text, __web_link text, __local_link text,
                                           __other_data json, __pub_date timestamp without time zone,
                                           __load_date timestamp without time zone) returns boolean
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

create or replace function get_all_active_plugins()
    returns TABLE
            (
                plugin_id  integer,
                repository text,
                active     boolean,
                pub_date   timestamp without time zone
            )
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

create or replace function set_plugin_pub_date(__plugin_id integer, __pub_date timestamp without time zone) returns void
    language plpgsql
as
$$
begin
    UPDATE public.spp_plugin as sp
    SET pub_date = __pub_date
    WHERE public.spp_plugin.plugin_id = __plugin_id;
end;
$$;

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

create or replace function set_task_status(__task_id integer, __status_code integer) returns boolean
    language plpgsql
as
$$
declare
    __status_id integer;
begin


    SELECT status_id INTO __status_id FROM public.spp_task_status WHERE code = __status_code;

    UPDATE public.spp_task
    SET status_id = __status_id
    WHERE id = __task_id;
    return TRUE;
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

create or replace function set_next_launch_time(__task_id integer, __next_time timestamp without time zone) returns boolean
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

create or replace function task_finish(__task_id integer, __restart_time interval) returns boolean
    language plpgsql
as
$$
declare
    __status_id            integer;
    __new_time_next_launch timestamp WITHOUT TIME ZONE;
    __last_finish_time     timestamp WITHOUT TIME ZONE;
begin


    SELECT status_id INTO __status_id FROM public.spp_task_status WHERE name LIKE 'FINISHED';
    SELECT now()::timestamp WITHOUT TIME ZONE INTO __last_finish_time;


    IF (__restart_time IS NULL) THEN
        UPDATE public.spp_task
        SET status_id        = __status_id,
            last_finish_time = __last_finish_time
        WHERE id = __task_id;
    ELSE
        __new_time_next_launch := __last_finish_time + __restart_time;

        UPDATE public.spp_task
        SET status_id        = __status_id,
            last_finish_time = __last_finish_time,
            time_next_launch = __new_time_next_launch
        WHERE id = __task_id;
    end IF;
    return TRUE;
end;
$$;

create or replace function relevant_plugins_for_processing()
    returns TABLE
            (
                plugin_id  integer,
                repository text,
                pub_date   timestamp without time zone,
                other_data json
            )
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
                          (st.status_id = 5 OR st.status_id = 6) AND st.time_next_launch < now()
                             )
                     );

end;
$$;

create or replace function create_task(__plugin_id integer, __time_next_launch timestamp without time zone,
                                       __status_code integer) returns integer
    language plpgsql
as
$$
declare
    __time           timestamp WITHOUT TIME ZONE;
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

