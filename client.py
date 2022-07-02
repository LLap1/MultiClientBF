from Abstract.Isocket import MySocket
import socket
import os
from mythread import MyThread
from brute_forcer import Brute_forcer
from threading import Thread
from myhash import MyHash


class Client(MySocket):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self._total_threads = int(os.cpu_count()) - 1  # 1 additional thread to listen for kill switch

    def connect(self):  # connecting to host
        try:
            self._socket.connect((self._ip, self._port))
        except socket.error as e:
            print(e)

        print(f"[+] connected to {self._ip}:{self._port}")

        # send thread count:
        data = f"THREADS:{self._total_threads}"
        self._send(data)

        # starting listening thread
        MyThread(self._listen).start()

    def _listen(self):  # listening for incoming data
        while 1:
            data = self._socket.recv(1024).decode()
            if data != "":
                code, *value = data.split(":")
                print("Server:", code, value)
                match code:
                    case "HASH":
                        _hash = value[0]
                        length = int(value[1])
                        alg = str(value[2])
                        self._myhash = MyHash(_hash, alg, length)
                    case "START":
                        # the range to brute force given to the client:
                        jobs_per_client = int(value[0])
                        charset = value[1]
                        self._brute_forcer = Brute_forcer(
                            self._myhash, self._total_threads, charset, jobs_per_client
                        )
                        print(f"[!] Starting to bruteforce: {self._myhash}")
                        self._brute_forcer.run()
                        MyThread(self._get_result).start()

                    case "STOP":
                        self._brute_forcer.stop()

    def _get_result(self):
        while self._myhash.plain_text == '':
            pass
        self._send("FOUND:" + self._myhash.plain_text)

    # properties:
    @property
    def total_threads(self):
        return self._total_threads


def initiate(c_socket):  # initiating the two sockets on different threads
    c_socket.connect()


if __name__ == '__main__':
    # c_socket1 = Client("127.0.0.1", 8090)
    c_socket2 = Client("127.0.0.1", 8090)

    # t1 = Thread(target=initiate, args=(c_socket1,)).start()
    t2 = Thread(target=initiate, args=(c_socket2,)).start()
