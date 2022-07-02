from Validators.validators import val_str, val_int

class MyHash:
    def __init__(self, _hash='', alg='', length=0):

        val_str(_hash=_hash)
        val_int(length=length)

        allowed_algs = ["sha1", "sha224", "sha256", "sha384", "sha512", "blake2b", "blake2s", "md5"]
        assert alg in allowed_algs, "new_alg is not supported!"

        self._hash = _hash
        self._length = int(length)
        self._alg = alg
        self._plain_text = ''

    @property
    def hash(self):
        return self._hash

    @property
    def length(self):
        return self._length

    @property
    def alg(self):
        return self._alg


    @property
    def plain_text(self):
        return self._plain_text

    @plain_text.setter
    def plain_text(self, hash_plain_text):
        val_str(hash_plain_text=hash_plain_text)
        self._plain_text = hash_plain_text



    def __str__(self):
        return f"{self.hash}:{self.plain_text} - length:{self.length}"