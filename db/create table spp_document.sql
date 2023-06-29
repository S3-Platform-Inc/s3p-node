-- Table: public.spp_document

-- DROP TABLE IF EXISTS public.spp_document;

CREATE TABLE IF NOT EXISTS public.spp_document
(
    doc_id serial PRIMARY KEY,
    title text NOT NULL,
    abstract text,
    text text,
    web_link text NOT NULL,
    local_link text,
    other_data json,
    pub_date timestamp without time zone NOT NULL,
    load_date timestamp without time zone,
    source_id integer NOT NULL,
    FOREIGN KEY (source_id)
        REFERENCES public.spp_source (source_id)
)