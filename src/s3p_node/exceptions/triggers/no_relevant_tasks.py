from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from s3p_sdk.types import S3PNode


class NoRelevantTasks(Exception):
    """Exception raised for errors in the trigger.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, node: S3PNode):
        self.node = node
        self.message = f"No relevant tasks for node: {node}"
        super().__init__(self.message)
