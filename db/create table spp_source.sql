-- Table: public.spp_source

-- DROP TABLE IF EXISTS public.spp_source;

CREATE TABLE IF NOT EXISTS public.spp_source
(
    source_id serial PRIMARY KEY,
    name text UNIQUE NOT NULL,
    config json,
    sphere text,
    load_date timestamp without time zone NOT NULL
);
