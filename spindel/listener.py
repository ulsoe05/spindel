from typing import Protocol
from enum import Enum, auto

from connection import Connection

class ListenerState(Enum):
    LISTENING = auto()
    CLOSED = auto()
    ERROR = auto()

class Listener(Protocol):
    def close(self) -> None: ...
    def accept(self) -> Connection: ...
    def fileno(self) -> int: ...
    def state(self) -> ListenerState: ...