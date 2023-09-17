create table if not exists spp_source
(
    source_id serial
        primary key,
    name      text      not null
        unique,
    config    json,
    sphere    text,
    load_date timestamp not null
);

alter table spp_source
    owner to sppuser;

create table if not exists spp_document
(
    doc_id     serial
        primary key,
    title      text      not null,
    abstract   text,
    text       text,
    web_link   text      not null,
    local_link text,
    other_data json,
    pub_date   timestamp not null,
    load_date  timestamp,
    source_id  integer   not null
        references spp_source
);

alter table spp_document
    owner to sppuser;

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

alter function safe_get_source(text) owner to sppuser;

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

alter function safe_init_document(integer, text, text, text, text, timestamp) owner to sppuser;

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

alter function get_all_documents_by_source(integer, text) owner to sppuser;

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

alter function safe_update_document(integer, text, integer, text, text, text, text, text, json, timestamp, timestamp) owner to sppuser;

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

alter function equal_documents(integer, text, text, timestamp, integer, integer, text, text, timestamp, integer) owner to sppuser;

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

alter function update_document(integer, text, integer, text, text, text, text, text, json, timestamp, timestamp) owner to sppuser;