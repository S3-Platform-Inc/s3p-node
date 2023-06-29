create function safe_init_document(__source_id integer, __sourcename text, __title text, __abstract text,
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

        insert into public.spp_document (doc_id, title, abstract, web_link, pub_date, source_id)
        VALUES (default, __title, __abstract, __web_link, __pub_date, temp_spource_id);

        return true;
    else
        return false;
    end if;
end;
$$;

alter function safe_init_document(integer, text, text, text, text, timestamp) owner to postgres;

