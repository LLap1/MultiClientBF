import sys

from mysocket import MySocket
import socket
import os
from brute_forcer import Brute_forcer
from threading import Thread


class Client(MySocket):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self._total_threads = int(os.cpu_count())

    def connect(self):  # connecting to host
        try:
            self._socket.connect((self._ip, self._port))
        except socket.error as e:
            print(e)

        print(f"[+] connected to {self._ip}:{self._port}")

        # send thread count:
        data = f"THREADS:{self._total_threads}".encode()
        self._socket.send(data)

        # starting listening thread
        Thread(target=self._listen).start()

    def _listen(self):  # listening for incoming data
        while 1:
            data = self._socket.recv(1024).decode()
            if data != "":
                code, *value = data.split(":")
                print("Server:", code, value)
                match code:
                    case "HASH":
                        self._myhash.hash = value[0]
                        self._myhash.length= int(value[1])
                        self._brute_forcer= Brute_forcer(self._myhash, self._total_threads)

                    case "START":
                        # the range to brute force given to the client:
                        self._brute_forcer.start = int(value[0])
                        self._brute_forcer.end = int(value[1])
                        print(f"[!] Starting to brute force!!!")
                        self._brute_forcer.run()
                        self._get_result()
                        break


    def _get_result(self):
        while not self._myhash.is_cracked:
            pass
        data = self._myhash.plain_text
        if data == '':
            self._send("NOTFOUND:", self._socket)
        else:
            self._send("FOUND:" + data, self._socket)

        print(data)



def initiate(c_socket):  # initiating the two sockets on different threads
    c_socket.connect()


if __name__ == '__main__':
    c_socket1 = Client("127.0.0.1", 8090)
    c_socket2 = Client("127.0.0.1", 8090)

    t1 = Thread(target=initiate, args=(c_socket1,)).start()
    t2 = Thread(target=initiate, args=(c_socket2,)).start()
