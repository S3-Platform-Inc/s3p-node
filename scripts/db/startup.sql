create schema nodes;

comment on schema nodes is 'Схема для представления и работы с функциями';

create schema tasks;

comment on schema tasks is 'Схема для представления и работы с задачами';

create schema plugins;

comment on schema plugins is 'Схема для представления и работы с плагинами';

create schema sources;

comment on schema sources is 'схема для представления и работы с источниками';

create schema ml;

comment on schema ml is 'Схема для представления и работы с ml';

create schema documents;

comment on schema documents is 'Схема для представления и работы с документами';

create schema analytics;

create user "sppTgBot";

comment on role "sppTgBot" is 'login for users tg bot';


create sequence tasks.sessions_n_session_id_seq
    as integer;

create table if not exists nodes.node
(
    id     serial
        primary key,
    name   text not null,
    ip     text,
    config json
);

create table if not exists nodes.sessions
(
    id     serial
        primary key,
    start  timestamp with time zone not null,
    stop   timestamp with time zone,
    alive  timestamp with time zone,
    nodeid serial
        references nodes.node
);

create table if not exists plugins.plugin
(
    id         serial
        primary key,
    repository text    not null,
    active     boolean not null,
    loaded     timestamp with time zone,
    config     json
);

create table if not exists tasks.status
(
    code integer not null
        primary key,
    name text    not null
        constraint status_pk
            unique
);

create table if not exists tasks.errors
(
    id       serial
        primary key,
    datetime timestamp with time zone not null,
    comment  text                     not null,
    taskid   serial
);

create table if not exists tasks.schedule
(
    id     serial
        primary key,
    start  timestamp with time zone not null,
    taskid serial
);

create table if not exists ml.model
(
    id     serial
        primary key,
    name   text,
    config json
);

create table if not exists sources.source
(
    id      serial
        primary key,
    name    text not null,
    sphere  text,
    created timestamp with time zone
);

grant select on sources.source to "sppTgBot";

create table if not exists documents.document
(
    id          serial
        primary key,
    sourceid    serial
        references sources.source,
    title       text                     not null,
    weblink     text                     not null,
    published   timestamp with time zone not null,
    abstract    text,
    text        text,
    storagelink text,
    loaded      timestamp with time zone,
    otherdata   json
);

grant select on documents.document to "sppTgBot";

create table if not exists ml.plugin
(
    modelid serial
        references ml.model,
    primary key (id)
)
    inherits (plugins.plugin);

create table if not exists sources.plugin
(
    sourceid serial
        references sources.source,
    primary key (id)
)
    inherits (plugins.plugin);

create table if not exists tasks.task
(
    id       serial
        primary key,
    status   integer not null
        references tasks.status,
    pluginid integer not null
        unique
);

create table if not exists tasks.sessions
(
    id           serial
        primary key,
    start        timestamp with time zone not null,
    stop         timestamp with time zone,
    taskid       serial
        constraint sessions_task_id_fk
            references tasks.task,
    n_session_id integer default nextval('tasks.sessions_n_session_id_seq'::regclass)
        references nodes.sessions
);

alter sequence tasks.sessions_n_session_id_seq owned by tasks.sessions.n_session_id;

create table if not exists ml.score
(
    id         serial
        primary key,
    score      json                     not null,
    date       timestamp with time zone not null,
    config     json,
    documentid serial
        references documents.document,
    pluginid   serial
        references ml.plugin
);

create table if not exists analytics.offload
(
    id     serial
        primary key,
    date   timestamp with time zone not null,
    params json
);

grant select, usage on sequence analytics.offload_id_seq to "sppTgBot";

grant insert, select on analytics.offload to "sppTgBot";

create table if not exists analytics.offloaded_documents
(
    document integer not null
        primary key
        references documents.document,
    offload  integer
        references analytics.offload
);

grant insert, select on analytics.offloaded_documents to "sppTgBot";

create or replace view plugins.complete(tid, status, pid, repository, loaded, config, type, refid, refname) as
SELECT task.id AS tid,
       task.status,
       pl.id   AS pid,
       pl.repository,
       pl.loaded,
       pl.config,
       pl.type,
       pl.refid,
       pl.refname
FROM tasks.task
         JOIN (SELECT plugin.id,
                      plugin.repository,
                      plugin.loaded,
                      plugin.config,
                      'SOURCE'::text                      AS type,
                      plugin.sourceid                     AS refid,
                      (SELECT source.name
                       FROM sources.source
                       WHERE source.id = plugin.sourceid) AS refname
               FROM sources.plugin
               UNION ALL
               SELECT plugin.id,
                      plugin.repository,
                      plugin.loaded,
                      plugin.config,
                      'ML'::text                        AS type,
                      plugin.modelid                    AS refid,
                      (SELECT model.name
                       FROM ml.model
                       WHERE model.id = plugin.modelid) AS refname
               FROM ml.plugin) pl ON task.pluginid = pl.id;

comment on view plugins.complete is 'Выбирает задачи и добавляет к ним данные о плагине и связанным с ним объектом (источник, модель, pipeline)';

create or replace function nodes.active_sessions()
    returns TABLE(session_id integer, node_id integer, alive timestamp with time zone)
    language plpgsql
as
$$
begin
    RETURN QUERY SELECT ns.id, ns.nodeid, ns.alive as alive
                 FROM nodes.sessions ns
                 WHERE (ns.alive is NOT NULL AND ns.stop IS NULL AND ns.start < NOW());
end;
$$;

comment on function nodes.active_sessions() is 'Возвращает таблицу со всеми активными сессиями всех узлов';

create or replace function nodes.active_session(nodeid integer) returns integer
    language plpgsql
as
$$
    declare sid integer;
begin

    select session_id into sid from nodes.active_sessions() where node_id = nodeid ORDER BY alive DESC LIMIT 1;
    RETURN sid;
end;
$$;

comment on function nodes.active_session(integer) is 'Возвращает id активной сессии узла по его id (передаваемый параметр)';

create or replace function nodes.alive(__id integer) returns integer
    language plpgsql
as
$$
    declare
        sid integer;
begin
    select nodes.active_session(__id) into sid;
    if (sid IS NULL)
    THEN
        insert into nodes.sessions(start, nodeid, alive)
        VALUES (now(), __id, now());
    end if;

    UPDATE nodes.sessions SET alive = now() WHERE id = sid;

    return sid;
end;
$$;

comment on function nodes.alive(integer) is 'Функция, которую вызывает узел SPP для обновления статуса "я жив"';

create or replace function nodes.observe_node_session() returns integer
    language plpgsql
as
$$
    declare
        dead_sessions integer;
begin

    SELECT COUNT(*) into dead_sessions FROM nodes.active_sessions() n, LATERAL nodes.kill_session(n.session_id) sid WHERE AGE(now(), alive) > '3 secs'::interval;

--     SELECT sid FROM nodes.active_sessions() n, LATERAL nodes.kill_session(n.session_id) sid WHERE AGE(now(), alive) > interval '3 secs';

    return dead_sessions;
end;
$$;

comment on function nodes.observe_node_session() is 'Просматривает все активные сессии и проверяет, чтобы дата последнего обновления статуса "я жив" узла SPP был не больше N секунд. Если находятся сессии, чей статус не обновился, то для этой сессии вызывается функция nodes.kill_session(id integer)';

create or replace function nodes.kill_session(__id integer) returns integer
    language plpgsql
as
$$
begin
    UPDATE nodes.sessions SET alive = NULL, stop = now() WHERE id = __id;
    return __id;
end;
$$;

comment on function nodes.kill_session(integer) is 'Фукнция для уничтожения активной сессии узла SPP';

create or replace function tasks.add_task(__pluginid integer, iscreateschedule boolean) returns integer
    language plpgsql
as
$$
    declare
        tid integer;
begin
    INSERT INTO tasks.task (status, pluginid) values (0, __pluginID) RETURNING id into tid;

    IF isCreateSchedule is true THEN
        perform tasks.schedule(tid, null);
    end if;

    return tid;
end
$$;

create or replace function plugins.on_addition_plugin() returns trigger
    language plpgsql
as
$$
begin

    if not EXISTS(select *
                  FROM tasks.task t
                  WHERE t.pluginid = new.id)
    THEN
--         Добавлен плагин, задача для которого не была создана
        perform tasks.add_task(new.id, new.active);
    end if;

--     perform public.observe_plugins();

    return new;
end
$$;

create trigger plugin_insert_observer
    after insert
    on plugins.plugin
execute procedure plugins.on_addition_plugin();

create trigger ml_plugin_insert_observer
    after insert
    on ml.plugin
    for each row
execute procedure plugins.on_addition_plugin();

create trigger s_plugin_insert_observer
    after insert
    on sources.plugin
    for each row
execute procedure plugins.on_addition_plugin();

create or replace function plugins.plugin_update_active() returns trigger
    language plpgsql
as
$$
    declare tid integer;
begin

    select id into tid from tasks.task where pluginid = new."id";

    if (new.active is true) then
        perform tasks.schedule(tid, now());
    else
        perform * from tasks.schedule sch, lateral tasks.unschedule(sch.id, 80) where sch.taskid = tid;
    end if;

    return new;
end
$$;

create trigger plugin_update_observer
    after update
        of active
    on plugins.plugin
    for each row
execute procedure plugins.plugin_update_active();

create trigger s_plugin_update_observer
    after update
        of active
    on ml.plugin
    for each row
execute procedure plugins.plugin_update_active();

create trigger s_plugin_update_observer
    after update
        of active
    on sources.plugin
    for each row
execute procedure plugins.plugin_update_active();

create or replace function tasks.check_add_task() returns trigger
    language plpgsql
as
$$
    declare pluginIdExists boolean;
begin
    select (pl.id is not null) from plugins.plugin pl where pl.id = new.pluginid into pluginIdExists;
    if (pluginIdExists) then
        return NEW;
    else
        raise exception 'Nonexistent ID --> %', new.pluginid;
        return null;
    end if;
end
$$;

create trigger pluginid_add_task_check
    before insert or update
    on tasks.task
    for each row
execute procedure tasks.check_add_task();

create or replace function tasks.schedule(taskid integer, start timestamp with time zone) returns integer
    language plpgsql
as
$$
    declare schID integer;
begin

    if (start is null) then
--         Если время запуска не указана, то выбрать текущее время
        start := now();
    end if;
    if (start < now()) then
        raise exception 'Start time --> % in the past', start;
    end if;

    insert into tasks.schedule (start, taskid) values (start, schedule.taskID) returning schedule.id into schID;
    UPDATE tasks.task t set status = 10 where t.id = taskID;

    return schID;
end
$$;

create or replace function tasks.unschedule(scheduleid integer, _status integer) returns integer
    language plpgsql
as
$$
begin

    if (_status is not null) then
--         Изменение статуса при необходимости
        perform tasks.set_status((select taskid from tasks.schedule where id = scheduleID), _status);
    end if;

--     Удаление записи из таблицы расписания
    delete from tasks.schedule where id = scheduleID;

    return scheduleID;
end
$$;

create or replace function tasks.set_status(taskid integer, _status integer) returns integer
    language plpgsql
as
$$
begin

    UPDATE tasks.task set status = _status where id = taskID;
    return taskID;
end
$$;

create or replace function nodes.plugin_types(nodeid integer)
    returns TABLE(type text)
    language plpgsql
as
$$
begin
    return query select value as type from json_array_elements_text((select config -> 'plugins' -> 'types' from nodes.node where id = nodeID));
end
$$;

create or replace function nodes.init(__name text, __ip text, __config json) returns integer
    language plpgsql
as
$$
    declare
        __id integer;
begin
    if not EXISTS(select *
                  FROM nodes.node
                  WHERE name = __name)
    THEN

        insert into nodes.node (name, ip, config)
        VALUES (__name, __ip, __config);

        RETURN currval('nodes.node_id_seq');
    else
        select id into __id
                  FROM nodes.node
                  WHERE name = __name;
        return __id;
    end if;
end;
$$;

create or replace function tasks.broke(nodeid integer, sessionid integer, comment text) returns integer
    language plpgsql
as
$$
    declare _tid integer;
begin
    UPDATE tasks.sessions set stop = now() where id = broke.sessionID;
    UPDATE tasks.task set status = 60 where id = (select taskid from tasks.sessions where id = broke.sessionID) returning id into _tid;

    insert into tasks.errors (datetime, comment, taskid) values (now(), broke.comment, _tid);
    return _tid;
end
$$;

create or replace function plugins.timer(id integer) returns interval
    language plpgsql
as
$$
    declare int interval;
begin
    select (config -> 'task' -> 'trigger' ->> 'interval')::interval into int from plugins.plugin where plugin.id = timer.id limit 1;
    return int;
end
$$;

create or replace function tasks.finish(nodeid integer, sessionid integer) returns integer
    language plpgsql
as
$$
    declare _tid integer; _pid integer;
begin
    UPDATE tasks.sessions set stop = now() where id = finish.sessionID; -- // Завершение текущей сессии
    UPDATE tasks.task set status = 50
                      where id = (select taskid from tasks.sessions where id = finish.sessionID)
                      returning id into _tid; -- // Обновление статуса задача на 'finished'
    select pc.pid into _pid from plugins.complete pc where pc.tid = _tid;

    if (select * from plugins.timer(_pid)) is not null then
        perform tasks.schedule(_tid, now() + (select * from plugins.timer(_pid))); -- // Добавление нового расписания
    end if;

    return _tid;

end
$$;

create or replace function tasks.relevant(nodeid integer)
    returns TABLE(sessionid integer, taskid integer, taskstatus integer, pluginid integer, repository text, loaded timestamp with time zone, config json, type text, referenceid integer, referencename text)
    language plpgsql
as
$$
    declare
        _tid integer; _schid integer; _tsession integer; _pluginId integer;
begin
--         Эта функция должна выбрать одну задачу, основываясь на таблице расписания. Удалить выбранную запись расписания, собрать данные о задаче и об плагине этой задачи и вернуть их в форме таблицы.

--     Выбираются такие задачи, для которых плагин имеет тип, который поддерживает узел. При этом на полученные задачи должно иметься расписание. Затем выбирается одна старая запланированная задача.
    select sch.id, pl.tid, pl.pid into _schid, _tid, _pluginId from plugins.complete pl
        left join tasks.schedule sch on sch.taskid = pl.tid
             where
                 pl.type in (select * from nodes.plugin_types(nodeID))
                 and sch.id is not null
                 and sch.start < now()
             order by sch.start
             limit 1;

--     select schedule.id, schedule.taskid into schid, tid from tasks.schedule where tasks.schedule.start < now() order by schedule.start limit 1;
    if (_schid is null) then
--         Если не было получена запись расписания, значит нет задач для запуска
        return;
    end if;

    perform tasks.set_status(_tid, 20); -- // Задача перешла в режим "получена" (<given> status)
    perform tasks.unschedule(_schid, null); -- // удаление записи расписания

    insert into tasks.sessions (start, stop, taskid, n_session_id)
        values (
                now(),
                null,
                _tid,
                null
        )
        returning id into _tsession; -- // Создание сессии задачи и получение id новой сессии
    return query select _tsession as sessionid, * from plugins.complete where complete.tid = _tid; -- // полные данные о задаче с ID сессии этой задачи
end
$$;

create or replace function documents.equals(lhid integer, lhtitle text, lhweblink text, lhpubdate timestamp with time zone, lhsource integer, rhid integer, rhtitle text, rhweblink text, rhpubdate timestamp with time zone, rhsource integer) returns boolean
    language plpgsql
as
$$

begin

    --     1. Сначала проверяем совпадают ли у документов источники
--     Если источники документов не равны, то ДОКУМЕНТЫ НЕ РАВНЫ
    IF (lhSource <> rhSource) THEN
        RETURN FALSE;
    end if;

--      2. Проверяем есть ли у документов поле ID. Если у какого-нибудь документа поля ID нет, то проверять соответствие будем по 3 уникальным полям, который должны быть.
    IF (lhID IS NULL) OR (rhID IS NULL) THEN
        RETURN (lhTitle = rhTitle) AND (lhWebLink = rhWebLink) AND (lhPubDate = rhPubDate);
    end if;

--      3. Если у двух документов есть ID, то сравнение происходит по ним
    IF (lhID IS NOT NULL) AND (rhID IS NOT NULL) THEN
        RETURN lhID = rhID;
    end if;

    RETURN FALSE;
end;
$$;

create or replace function documents.save(sourceid integer, newtitle text, newabstract text, newtext text, newweblink text, newlocallink text, newotherdata json, newpubdate timestamp with time zone, newloaddate timestamp with time zone) returns integer
    language plpgsql
as
$$
declare
    docID INTEGER;

begin

    select id into docID FROM documents.document d
             WHERE d.sourceid = save.sourceID
               AND d.title = save.newTitle
               AND d.weblink = save.newWeblink
               AND d.published = save.newPubDate;

    if (docID is null) then
        insert into documents.document (sourceid, title, weblink, published, abstract, text, storagelink, loaded, otherdata)
        VALUES (save.sourceID, newTitle, newWeblink, newPubDate, newAbstract, newText, newLocalLink, newLoadDate, newOtherData) returning id into docID;
    else
        update documents.document d set
                                      abstract = newAbstract,
                                      text = newText,
                                      storagelink = newLocalLink,
                                      loaded = newLoadDate,
                                      otherdata = newOtherData
        where d.id = docID;

    end if;

    return docID;
end;
$$;

create or replace function documents."all"(_sourceid integer)
    returns TABLE(id integer, sourceid integer, title text, weblink text, published timestamp with time zone, abstract text, text text, storagelink text, loaded timestamp with time zone, otherdata json)
    language plpgsql
as
$$
begin
--     Фукнция для получения всех документов.
--          Если источник указан, то выбираются все документы этого источника
--          Если источник не указан, то выдаются все документы
    return query select * from documents.document d
                          where (_sourceID is NULL) or (_sourceID = d.sourceid);
end
$$;

create or replace function documents.littles(_sourceid integer)
    returns TABLE(id integer, sourceid integer, title text, weblink text, published timestamp with time zone)
    language plpgsql
as
$$
begin
--     Функция возвращает все документы (как в функции documents."all"), но обрезает, чтобы уменьшить размер получаемого пакета
--          такая функция используется там, где нужно сравнить документы (например, в модуле фильтрации платформы)
    return query select "all".id, "all".sourceid, "all".title, "all".weblink, "all".published from documents.all(_sourceid);
end
$$;

create or replace function analytics.offload_document(offloadid integer, documentid integer) returns integer
    language plpgsql
as
$$
    declare __id integer;
begin
--         Добавление новой выгрузки
    insert into analytics.offloaded_documents (document, offload) VALUES (documentID, offloadID) returning document into __id;
    return 1;
end
$$;

grant execute on function analytics.offload_document(integer, integer) to "sppTgBot" with grant option;

create or replace function analytics.export(export_id integer)
    returns TABLE(id integer, title text, weblink text, published timestamp with time zone, abstract text, text text, storagelink text, loaded timestamp with time zone, otherdata json, source_id integer, source_name text)
    language plpgsql
as
$$
    declare offid integer;
begin
--         Добавление новой выгрузки
    if (export_id is NULL) then
        if exists(select * from documents.document d where d.id not in (select document from analytics.offloaded_documents)) then
            insert into analytics.offload (date) VALUES (now()) returning offload.id into offid;
            return query select d.id, d.title, d.weblink, d.published, d.abstract, d.text, d.storagelink, d.loaded, d.otherdata, s.id, s.name
                     from documents.document d join sources.source s on d.sourceid = s.id,
                         lateral analytics.offload_document(offid, d.id)
                     where d.id not in (select document from analytics.offloaded_documents);
        end if;
    else
        return query select d.id, d.title, d.weblink, d.published, d.abstract, d.text, d.storagelink, d.loaded, d.otherdata, s.id, s.name
                         from analytics.offloaded_documents offdoc left join documents.document d on offdoc.document = d.id join sources.source s on s.id = d.sourceid
                         where offdoc.offload = export_id;
    end if;
end
$$;

create or replace function analytics.export_lists()
    returns TABLE(id integer, date timestamp with time zone, count bigint)
    language plpgsql
as
$$
begin
    return query select o.id, o.date, count(*) from analytics.offload o left join analytics.offloaded_documents od on o.id = od.offload
                 group by o.id order by o.id;
end
$$;

