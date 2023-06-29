create function get_all_documents_by_source(__source_id integer, __sourcename text)
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
                s_id       integer,
                s_name     text,
                s_config   json,
                s_sphere   text
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
                        sd.load_date,
                        sd.other_data,
                        sd.pub_date,
                        ss.source_id as s_id,
                        ss.name      as s_name,
                        ss.config    as s_config,
                        ss.sphere    as s_sphere
                 from public.spp_document as sd
                          JOIN spp_source as ss
                               on ss.source_id = sd.source_id
                 WHERE ss.source_id = temp_spource_id;
end;
$$;

alter function get_all_documents_by_source(integer, text) owner to postgres;

