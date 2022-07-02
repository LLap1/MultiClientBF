import socket

def val_str(**kwargs): # validating str variables
    for pair in kwargs.items():
        name, value = pair
        assert isinstance(value, str), f"{name} must be str!"


def val_int(**kwargs): # validating int variables
    for pair in kwargs.items():
        name, value = pair
        assert isinstance(value, int), f"{name} must be int!"


def val_num(**kwargs):
    for pair in kwargs.items():
        name, value = pair
        assert value.isnumeric(), f"{name} must be  numeric!"


def val_bool(**kwargs):
    for pair in kwargs.items():
        name, value = pair
        assert value.isnumeric(), f"{name} must be boolean!"


def val_function(**kwargs):
    for pair in kwargs.items():
        name, value = pair
        assert callable(value), f"{name} must be callable!"

def val_socket(**kwargs):
    for pair in kwargs.items():
        name, value = pair
        assert isinstance(value, socket.socket), f"{name} must of type socket!"