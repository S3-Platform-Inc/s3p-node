

class NoCurrentTasks(Exception):
    """Exception raised for errors in the trigger.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, tid: int):
        self.tid = tid
        self.message = f"No current tasks by ID: {tid}"
        super().__init__(self.message)
