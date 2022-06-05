class MyHash:
    def __init__(self, _hash='', length=0):
        self._hash= _hash
        self._length = int(length)
        self._plain_text = ''

    @property
    def hash(self):
        return self._hash

    @property
    def length(self):
        return self._length

    @property
    def is_cracked(self):
        return not self._plain_text == ''

    @property
    def plain_text(self):
        return self._plain_text

    @plain_text.setter
    def plain_text(self, hash_plain_text):
        self._plain_text = hash_plain_text

    @hash.setter
    def hash(self, new_hash):
        self._hash = new_hash

    @length.setter
    def length(self, new_length):
        assert isinstance(new_length, int)
        self._length = new_length

    def __str__(self):
        return f"{self.hash}:{self.plain_text} - length = {self.length}"