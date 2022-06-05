
def val_str(**kwargs): # validating str variables
    for pair in kwargs.items():
        name, value = pair
        assert isinstance(value, str), f"{name} must be of type str!"


def val_int(**kwargs): # validating int variables
    for pair in kwargs.items():
        name, value = pair
        assert isinstance(value, int), f"{name} must be of type int!"


def val_num(**kwargs):
    for pair in kwargs.items():
        name, value = pair
        assert value.isnumeric(), f"{name} must be of numeric!"
