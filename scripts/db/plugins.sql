TRUNCATE TABLE public.spp_task RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.spp_plugin RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.spp_source RESTART IDENTITY CASCADE;

INSERT INTO public.spp_source (name, load_date) VALUES ('test-source-1', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-testcase1', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('pci', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-pci', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('nist', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-nist', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('w3c', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-w3c', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('iso20022', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-iso20022', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('emvco', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-EMVCo', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('finextra', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-finextra', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('iso', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-iso', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('paypers', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-paypers', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('bis', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-bis', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('the-berlin-group', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-berlin-group', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('cen&cenelec', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-cen-cenelec', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('fintechfutures', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-fintechfutures', false, currval('spp_source_source_id_seq'), 1);

-- Verified plugins for testing
INSERT INTO public.spp_source (name, load_date) VALUES ('ecb', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-ecb', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('visa', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-visa', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('pwc', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-pwc', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('openbanking', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-openbanking', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('kpmg', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-kpmg', false, currval('spp_source_source_id_seq'), 1);

INSERT INTO public.spp_source (name, load_date) VALUES ('jcb', now());
INSERT INTO public.spp_plugin (repository, active, source_id, type) VALUES ('CuberHuber/NSPK-DI-SPP-plugin-jcb', false, currval('spp_source_source_id_seq'), 1);