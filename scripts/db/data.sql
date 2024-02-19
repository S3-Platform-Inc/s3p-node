-- необходимо запустить после инициализации базы данных и завершения инициализирующих скриптов


-- установка локального timezone
alter database "sppIntegrateDB" set timezone to 'Europe/Moscow';
set timezone to 'Europe/Moscow';


-- установка статусов задачи
INSERT INTO tasks.status(code, name) VALUES (0, 'noneset');
INSERT INTO tasks.status(code, name) VALUES (10, 'scheduled');
INSERT INTO tasks.status(code, name) VALUES (20, 'given');
INSERT INTO tasks.status(code, name) VALUES (30, 'preparing');
INSERT INTO tasks.status(code, name) VALUES (40, 'working');
INSERT INTO tasks.status(code, name) VALUES (50, 'finish');
INSERT INTO tasks.status(code, name) VALUES (60, 'broken');
INSERT INTO tasks.status(code, name) VALUES (70, 'terminated');
INSERT INTO tasks.status(code, name) VALUES (80, 'deactivated');