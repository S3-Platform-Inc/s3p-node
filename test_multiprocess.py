import multiprocessing
import time


class Task(multiprocessing.Process):

    def __init__(self, plugin, sleep, loop):
        super().__init__()
        self.plugin = plugin
        self.sleep = sleep
        self.loop = loop

    def run(self):
        print(f'Старт процесса №{self.name}')
        for i in range(self.loop):
            print(str(self.plugin), f'| loop {i}')
            time.sleep(self.sleep)
        print(f'Завершение работы процесса №{self.name}')


class TaskPool(multiprocessing.Pool):

    def __init__(self): ...


class TaskController:
    processes: dict[str, Task] = {}

    def __init__(self):
        ...

    def all(self):
        print(self.processes)

    def start_all(self):
        [process.start() for process in self.processes.values()]

    def status(self):
        for process in self.processes.values():
            print(process.name, process.exitcode)

    def add(self, task: Task):
        self.processes[task.name] = task

    def start(self, name: str):
        self.processes.get(name).start()

    def stop(self, name: str):
        self.processes.get(name).join()

    def terminate(self, name):
        self.processes.get(name).terminate()

    def close(self, name):
        self.processes.get(name).close()

    def processing(self):
        return any([process.is_alive() for process in self.processes.values()])


if __name__ == "__main__":
    tc = TaskController()

    tc.add(Task('PCI', 2, 4))
    tc.add(Task('NIST', 1, 4))

    tc.status()
    tc.start_all()
    i = 0
    while tc.processing():
        if i == 5:
            tc.terminate('Task-1')
        i += 1
        tc.status()
        time.sleep(1)

    tc.terminate('Task-2')
    tc.close('Task-1')
    tc.status()
