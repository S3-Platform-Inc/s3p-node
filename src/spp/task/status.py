NONSET = 0  # Задача создана и записана в таблицу БД.
SCHEDULED = 10  # Задача добавлена на исполнение и ожидает запуска по расписанию
GIVEN = 20  # Задача была выдана узлу SPP по запросу
PREPARING = 30  # Задача получена узлом и готовиться к запуску
WORKING = 40  # Задача запущена на узле на исполнение
FINISHED = 50  # Задача завершена успешно
BROKEN = 60  # Задача завершена с ошибкой или прервана
TERMINATED = 70  # Узел, на которой работала задача был убит
DEACTIVATED = 80  # Задача деактивирована.
# С этим состоянием она не может оказаться на узле (но пусть статус будет, чтобы знать о нем) :-)

_statusToName = {
    NONSET: "NONSET",
    SCHEDULED: "SCHEDULED",
    GIVEN: "GIVEN",
    PREPARING: "PREPARING",
    WORKING: "WORKING",
    FINISHED: "FINISHED",
    BROKEN: "BROKEN",
    TERMINATED: "TERMINATED",
    DEACTIVATED: "DEACTIVATED",
}

_nameToStatus = {
    "NONSET": NONSET,
    "SCHEDULED": SCHEDULED,
    "GIVEN": GIVEN,
    "PREPARING": PREPARING,
    "WORKING": WORKING,
    "FINISHED": FINISHED,
    "BROKEN": BROKEN,
    "TERMINATED": TERMINATED,
    "DEACTIVATED": DEACTIVATED,
}
