import socket
from threading import Condition, Thread

host_found_condition = Condition()


class Scanner:
    ip = None

    @staticmethod
    def try_connection(ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex((ip, port))
        if result == 0:
            with host_found_condition:
                Scanner.ip = ip
                host_found_condition.notifyAll()

    @staticmethod
    def get_ip(port=2222, timeout=10):
        socket.setdefaulttimeout(timeout)

        for sub in range(2):
            for sub2 in range(256):
                ip = f"192.168.{sub}.{sub2}"
                Thread(
                    target=Scanner.try_connection,
                    args=(
                        ip,
                        port,
                    ),
                ).start()

        with host_found_condition:
            host_found_condition.wait(timeout=timeout)

        return Scanner.ip
