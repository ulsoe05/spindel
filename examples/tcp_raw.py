from spindel import TcpConnection, TcpListener, ListenerState


def example():
    from test_log import make_logger
    from threading import Thread

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
    client_thread = Thread(target=client_func)
    client_thread.start()
    server_thread.join()
    client_thread.join()


if __name__ == "__main__":
    example()
