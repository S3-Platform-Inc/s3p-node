CREATE OR REPLACE FUNCTION public.safe_get_source(__sourcename TEXT)
    RETURNS TABLE
            (
                source_id  integer,
                sourcename TEXT,
                config     JSON,
                sphere     TEXT,
                load_date  TIMESTAMP
            )
    LANGUAGE plpgsql
AS
$$
begin
    IF EXISTS (select *
               from public.spp_source
               where name LIKE __sourcename)
    THEN
        return query select *
                     from public.spp_source
                     where name LIKE __sourcename;
    ELSE
        INSERT INTO public.spp_source(source_id, name, load_date) values (default, __sourcename, NOW());

        return query select s.source_id,
                            s.name,
                            s.config,
                            s.sphere,
                            s.load_date
                     from public.spp_source as s
                     where name LIKE __sourcename;
    END IF;
end;
$$