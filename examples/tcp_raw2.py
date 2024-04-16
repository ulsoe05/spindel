import logging
from spindel import TcpConnection, TcpListener, ListenerState, ConnectionState


def example():
    from test_log import make_logger
    from threading import Thread
    from time import perf_counter, sleep

    serverlog = make_logger(name="server", color="yellow", loglevel=logging.INFO)
    clientlog = make_logger(name="client", color="green", loglevel=logging.INFO)

    def server_func():
        t1 = perf_counter()
        listener = TcpListener("localhost", 8080, log=serverlog)
        while perf_counter() - t1 < 1:
            if listener.state() == ListenerState.LISTENING:
                connection = listener.accept()
                if connection is None:
                    continue
                serverlog.info(f"Accepted connection from {connection._host}:{connection._port}")
                connection.send_binary(b"Hello, world 1")
                connection.send_binary(b"Hello, world 2")
                connection.send_binary(b"Hello, world 3")
                sleep(0.001)
                connection.send_binary(b"Hello, world 4")
                connection.send_binary(b"Hello, world 5")
                connection.send_binary(b"Hello, world 6")
                sleep(0.001)

                connection.close()                
            sleep(0.001)
        listener.close()

    def client_func():
        t1 = perf_counter()
        connection = TcpConnection("localhost", 8080, log=clientlog)
        while perf_counter() - t1 < 1.0:
            clientlog.info(f"Connected to {connection._host}:{connection._port}")
            sleep(0.001)
            data = connection.recv_binary(1024)
            clientlog.info(f"Received: {data.decode()}")
        connection.close()

    server_thread = Thread(target=server_func)
    server_thread.start()
    client_thread = Thread(target=client_func)
    client_thread.start()
    server_thread.join()
    client_thread.join()


if __name__ == "__main__":
    example()
