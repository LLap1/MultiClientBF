from mysocket import MySocket
import socket
from validators import val_num
from mythread import MyThread as myThread

class Server(MySocket):
    def __init__(self, ip, port, _hash='', length=0):
        super().__init__(ip, port, _hash, length)

        self._c_dict = {}  # pair of client and thread count pair
        self._c_count = 0  # client count  connected to the server

    def host(self):
        try:
            print(f"[+] Starting a server at: {self._ip}:{self._port}")
            self._socket.bind((self._ip, self._port))
        except socket.error as e:
            print(e)

        # setting up a thread to wait for user input to start bruteforce
        myThread(self._brute_force_start).start()

        # setting up a thread to listen for incoming connections
        myThread(self._listen_conn).start()


    def _listen_conn(self):  # listening for new connections
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

            #creating a listening thread for incoming data from the new c_socket
            myThread(self._listen, args=(c_socket,)).start()

            # sending hash info:
            hash_info = f"HASH:{self._myhash.hash}:{self._myhash.length}"
            self._send(hash_info, c_socket)

    def _listen(self, c_socket):  # listen to data incoming from certain socket
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
                        print(f"[!]Hash Cracked By Client {c_num} - {value[0]}:{value[1]}")

                    case "NOTFOUND":
                        print(f"[!]Clients couldnt crack hash - {self._myhash.hash}")

    def _brute_force_start(self):  # wait for input from the user to start brute forcing
        choice = ''
        while choice != "start":
            choice = input("Enter 'start' when you want to start bruteforce!!\n")

        # Sending each client their brute force range and a start command
        start = 0
        possabilities = int("9" * self._myhash.length)

        for i, pair in enumerate(self._c_dict.items()):
            c_socket, threads = pair
            if i + 1 == len(self._c_dict):
                end = possabilities
            else:
                end = self._calc_end(threads, start=start)
            data = f"START:{start}:{end}"
            self._send(data, c_socket)
            start = end

    def _calc_end(self, threads, *, start=0):
        """
        Calculates an end point in the brute force list for client
        """
        end = start
        _range = int('9' * self._myhash.length)
        jobs = myThread.jobs_per_thread(_range, self._total_threads)

        end += jobs * threads
        possabilities = int("9" * self._myhash.length)

        if end > possabilities:
            return possabilities

        return end

    # Class properties:
    @property
    def _c_sockets(self):
        c_socket_list = [sock[0] for sock in self._c_dict.items()]
        return c_socket_list

    @property
    def _total_threads(self):
        thread_list = [sock[1] for sock in self._c_dict.items()]
        return sum(thread_list)

    # Class static methods:
    @staticmethod
    def _jobs_per_thread(range, threads):
        return int(range / threads)

if __name__ == '__main__':
    s_socket = Server("127.0.0.1", 8090, "25d55ad283aa400af464c76d713c07ad", 8)
    s_socket.host()
