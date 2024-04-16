from __future__ import annotations
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

    # Methods from Listener protocol
    def accept(self) -> TcpConnection | None:
        try:
            client_socket, address = self._socket.accept()
        except BlockingIOError:
            self.log.debug("No incoming connections")
            return None
        return TcpConnection.from_socket(client_socket, address, self.log)

    def close(self):
        self._socket.close()

    def fileno(self) -> int:
        return self._socket.fileno()

    def state(self) -> ListenerState:
        return self._state

    # Non-protocol methods
    def _get_socket_status(self) -> int:
        return self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

    def _listen(self):
        backlog = 15
        self._socket.listen(backlog)
        self._state = ListenerState.LISTENING


class TcpConnection:
    def __init__(self, host: str, port: int, log: Logger | None = None):
        self._host = host
        self._port = port
        self.log = getLogger() if log is None else log
        self._state = ConnectionState.PENDING_CONNECTION
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    # Methods from Connection protocol
    def close(self):
        self._socket.close()

    def send_binary(self, data):
        self._socket.sendall(data)

    def recv_binary(self, size) -> bytes:
        return self._socket.recv(size)

    def fileno(self) -> int:
        return self._socket.fileno()
    
    def state(self) -> ConnectionState:
        return self._state
    
    # Non-protocol methods
    @classmethod
    def from_socket(cls, socket: socket.socket, address: tuple[str, int], log: Logger):
        connection = cls.__new__(cls)
        connection._host = address[0]
        connection._port = address[1]
        connection.log = log
        connection._socket = socket
        connection._state = ConnectionState.PENDING_CONNECTION
        return connection






def example():
    from test_log import make_logger
    from threading import Thread
    import time

    serverlog = make_logger(name="server", color="yellow")
    clientlog = make_logger(name="client", color="green")

    def server_func():
        listener = TcpListener("localhost", 8080, log=serverlog)
        while True:
            if listener.state() == ListenerState.LISTENING:
                connection = listener.accept()
                if connection is None:
                    continue
                serverlog.info(f"Accepted connection from {connection._host}:{connection._port}")
                connection.send_binary(b"Hello, world!")
                connection.close()
                break
        listener.close()

    def client_func():
        connection = TcpConnection("localhost", 8080, log=clientlog)
        clientlog.info(f"Connected to {connection._host}:{connection._port}")
        data = connection.recv_binary(1024)
        clientlog.info(f"Received: {data.decode()}")
        connection.close()

    server_thread = Thread(target=server_func)
    server_thread.start()
    time.sleep(1.0)
    client_thread = Thread(target=client_func)
    client_thread.start()
    server_thread.join()
    client_thread.join()



if __name__ == "__main__":
    example()