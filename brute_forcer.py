from mythread import MyThread
import hashlib
from Validators.validators import val_str, val_int
from myhash import MyHash

class Brute_forcer:
    def __init__(self, myhash, total_threads, charset, jobs):

        assert isinstance(myhash, MyHash), "myhash must be instance of Myhash!"
        val_int(total_threads=total_threads, jobs=jobs)
        val_str(charset=charset)

        self._myhash = myhash # MyHash instance

        self._total_thread_count = total_threads # total threads avilable for brute-forcing
        self._hash_alg = hashlib.new(self._myhash.alg) # the hash algorithm

        self._jobs = jobs # amount of tries to check from generator
        self._charset = charset # the charset of the plain text
        self._gen = self._gen_build(self._charset) # the bruteforcing generator
        self._stop_switch = False # stop bruteforce switch



    def run(self):
        '''
        initiates the threads to run the bruteforce.
        splits the plain-text list to each thread.
        '''
        for i in range(self._total_thread_count - 1):
            print(f"[+]Thread - {i} initiated")
            MyThread(self._brute_force).start()

    def _gen_build(self, *charset):
        """
        :param charset: possible chars of the plaintext.
        :param start: the initial combination to start from.
        :param end: the last index of the combination to include.
        :param length: length of the plain text.
        :return: generator, product of the charset with a given length.
        """
        pools = [tuple(pool) for pool in charset] * self._myhash.length
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]

        for i, prod in enumerate(result):
            if i > self._jobs:
                break
            yield ''.join(prod)

    def _encrypt(self, plain_text):
        """
        :param plain_text: try to encrypted
        :return: hashed try
        """
        plain_text = ''.join(plain_text)
        enc_plain_text = plain_text.encode()
        self._hash_alg.update(enc_plain_text)
        _hash = self._hash_alg.hexdigest()
        return _hash

    def _brute_force(self):
        """
        starts to bruteforce.
        sets the kill-switch to True when plain text is found
        :return:
        """
        try:
            for plain_try in self._gen:
                hashed_try = self._encrypt(plain_try)
                if hashed_try == self._myhash.hash:
                    self._myhash.plain_text = plain_try
                    self._stop_switch = True
                if self._stop_switch:
                    break
        except ValueError:
            pass


    # Getters:
    @property
    def myhash(self):
        return self._myhash

    @property
    def total_thread_count(self):
        return self._total_thread_count

    @property
    def hash_alg(self):
        return self._hash_alg

    @property
    def jobs(self):
        return self._jobs

    @property
    def charset(self):
        return self._charset

    @property
    def stop_switch(self):
        return self._stop_switch

    # setters:
    @total_thread_count.setter
    def total_thread_count(self, new_thread_count):
        val_int(new_thread_count=new_thread_count)
        self._total_thread_count = new_thread_count

    @charset.setter
    def charset(self, new_charset):
        val_str(new_charset=new_charset)
        self._charset = new_charset


    def stop(self):
        self._stop_switch = False

    def start(self):
        self._stop_switch = True



