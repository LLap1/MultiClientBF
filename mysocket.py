from abc import ABC
import socket
from validators import val_str, val_int
from myhash import MyHash



class MySocket(ABC):
    def __init__(self, ip, port, _hash='', length=0):

        # validating parameters:
        val_int(port=port)
        val_str(ip=ip)
        # socket info:      server             client
        self._ip = ip # ip to host from / to connect to
        self._port = port # port to open / to connect to
        self._socket = socket.socket()
        # hash:
        self._myhash = MyHash(_hash, length)

    def _send(self, data, socket):
        socket.send(data.encode())

    @staticmethod
    def _send_socket(data, socket):
        socket.send(data.encode())

    # Class methods:
    def listen(self):
        """
        Opens a thread to handle incoming data.

        format:
        CODE:VALUE:SUB_VALUE(optional)

        returns:None
        """
        pass



