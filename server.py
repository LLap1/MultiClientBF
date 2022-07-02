import math
import string

from Abstract.Isocket import MySocket
from Validators.validators import *
from mythread import MyThread as myThread
from myhash import MyHash


class Server(MySocket):
    def __init__(self, ip, port, _hash):
        super().__init__(ip, port)

        self._c_dict = {}  # pair of client and thread count pair
        self._c_count = 0  # client count  connected to the server
        self._myhash = _hash  # hash to crack

    def host(self):
        try:
            print(f"[+] Starting a server at: {self._ip}:{self._port}")
            self._socket.bind((self._ip, self._port))
        except socket.error as e:
            print(e)

        # setting up a thread to wait for user input to start bruteforce
        myThread(self._brute_force_start).start()

        # setting up a thread to listen for incoming connections
        myThread(self._listen).start()


    def _listen(self):
        """
        listening for new connections
        :return:
        """
        while 1:
            try:
                self._socket.listen()
            except socket.error as e:
                print(e)

            c_socket, address = self._socket.accept()

            print(f"[!] Got connection from Client at: {address}")
            self._c_count += 1

            print(f"[+] Starting Threaded connection with Client {self._c_count}")
            print("Enter 'start' when you want to start bruteforce!!\n")

            # creating a listening thread for incoming data from the new c_socket
            myThread(self._listen_conn, args=(c_socket,)).start()

            # sending hash info:
            hash_info = f"HASH:{self._myhash.hash}:{self._myhash.length}:{self._myhash.alg}"
            self._send_to(hash_info, c_socket)

    def _listen_conn(self, c_socket):
        """
           listen to data incoming from certain socket
           :param c_socket: the socket that the server listens on for incoming data.
           :return:
        """
        val_socket(c_socket=c_socket)


        c_num = self._c_count
        while True:
            data = c_socket.recv(1024).decode()
            if data != "":
                code, *value = data.split(":")
                match code:
                    case "THREADS":
                        val_num(value=value[0])
                        self._c_dict[c_socket] = int(value[0])
                    case "FOUND":
                        print(f"[!] Hash Cracked By Client {c_num} - {self._myhash.hash}:{value[0]}")
                        self._send_kill_signal()
                    case "NOTFOUND":
                        print(f"[!] Clients couldnt crack hash - {self._myhash.hash}")

    def _brute_force_start(self):
        """
        wait for input from the user to start brute forcing
        :return:
        """
        choice = ''
        while choice != "start":
            choice = input("Enter 'start' when you want to start bruteforce!!\n")

        # Sending each client their brute force range and a start command
        charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
        total_jobs = int(math.pow(len(charset), self._myhash.length))
        jobs_per_client = int(total_jobs / self._c_count)

        for i, pair in enumerate(self._c_dict.items()):
            c_socket, threads = pair

            data = f"START:{jobs_per_client}:{charset}"
            charset = self._scramble_charset(charset)
            self._send_to(data, c_socket)

    def _send_kill_signal(self):
        """
        sending all the clients the kill signal, to stop brute-forcing
        :return:
        """
        for c_socket in self._c_dict.keys():
            self._send_to(f"STOP", c_socket)

    # Create charset for each client:
    def _scramble_charset(self, charset):
        val_str(charset=charset)
        """
        giving each client a scrambled charset in order to prevent clients from
        testing the same tries.
        :param charset: the charset we want to scramble
        :return: scrambled charset
        """
        scramble = int(len(charset) / self._c_count) + int(
            len(charset) / 2)  # the amount of times to scramble the charset.
        for i in range(scramble):
            charset = charset[-i:] + charset[:-i]
        return charset


if __name__ == '__main__':
    my_hash = MyHash("74b87337454200d4d33f80c4663dc5e5", "md5", 4)
    s_socket = Server("127.0.0.1", 8090, my_hash)
    s_socket.host()
