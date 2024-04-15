import socket
import os
from logging import Logger, getLogger
from connection import ConnectionState
from listener import ListenerState


class TcpListener:
    def __init__(self, host: str, port: int, log: Logger | None = None):
        self._host = host
        self._port = port
        self.log = getLogger() if log is None else log
        self._state = ListenerState.CLOSED

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(False)

        self._socket.settimeout(0)
        if os.name != "nt":
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self._socket.bind((host, port))
        except OSError as e:
            self.log.error(f"Failed to bind to {host}:{port}: {e}")
            self._state = ListenerState.ERROR
            return
        self._listen()

    def _get_socket_status(self) -> int:
        return self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

    def _listen(self):
        backlog = 15
        self._socket.listen(backlog)
        self._state = ListenerState.LISTENING

    def accept(self):
        client_socket, address = self._socket.accept()
        return TcpConnection.from_socket(client_socket, address, self.log)

    def close(self):
        self._socket.close()

    def fileno(self) -> int:
        return self._socket.fileno()

    def state(self) -> ListenerState:
        return self._state


class TcpConnection:
    def __init__(self, host: str, port: int, log: Logger | None = None):
        self._host = host
        self._port = port
        self.log = getLogger() if log is None else log
        self._state = ConnectionState.PENDING_CONNECTION
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    def send(self, data):
        self._socket.sendall(data)

    def receive(self, size):
        return self._socket.recv(size)

    def close(self):
        self._socket.close()

    @classmethod
    def from_socket(cls, socket: socket.socket, address: tuple[str, int], log: Logger):
        connection = cls.__new__(cls)
        connection._host = address[0]
        connection._port = address[1]
        connection.log = log
        connection._socket = socket
        connection._state = ConnectionState.PENDING_CONNECTION
        return connection
