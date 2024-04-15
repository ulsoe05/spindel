from typing import Protocol
from enum import Enum, auto


class ConnectionState(Enum):
    PENDING_CONNECTION = auto()
    CONNECTED = auto()
    OPEN = auto()
    CLOSED = auto()
    ERROR = auto()

class Connection(Protocol):
    def close(self) -> None: ...
    def send_binary(self, data: bytes) -> None: ...
    def recv_binary(self) -> bytes: ...
    def fileno(self) -> int: ...
    def state(self) -> ConnectionState: ...