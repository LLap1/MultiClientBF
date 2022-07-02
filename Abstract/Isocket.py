import abc
from abc import ABC
import socket
from Validators.validators import val_str, val_int



class MySocket(ABC):
    def __init__(self, ip, port):

        # validating parameters:
        val_int(port=port)
        val_str(ip=ip)


        # socket info:      server             client
        self._ip = ip # ip to host from / to connect to
        self._port = port # port to open / to connect to
        self._socket = socket.socket()



    def _send(self, data):
        self._socket.send(data.encode())

    @staticmethod
    def _send_to(data, socket): # sends the data through a specified socket.
        socket.send(data.encode())

    # Class methods:
    @abc.abstractmethod
    def _listen(self):
        """
        listen for incoming connection.
        returns:None
        """
        pass

    # Getters:
    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def socket(self):
        return self._socket

