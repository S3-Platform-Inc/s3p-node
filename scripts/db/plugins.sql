TRUNCATE TABLE public.spp_task RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.spp_plugin RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.spp_source RESTART IDENTITY CASCADE;

INSERT INTO public.spp_source (name, load_date) VALUES ('test-source-1', now());
INSERT INTO public.spp_plugin (repository, active, source_id) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-testcase1', false, currval('spp_source_source_id_seq'));

INSERT INTO public.spp_source (name, load_date) VALUES ('pci', now());
INSERT INTO public.spp_plugin (repository, active, source_id) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-pci', false, currval('spp_source_source_id_seq'));

INSERT INTO public.spp_source (name, load_date) VALUES ('nist', now());
INSERT INTO public.spp_plugin (repository, active, source_id) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-nist', false, currval('spp_source_source_id_seq'));

