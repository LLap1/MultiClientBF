from hashlib import md5
from mythread import MyThread as myThread


class Brute_forcer:

    def __init__(self, myhash, total_threads: int = 0, start=0, end=0):
        self._myhash = myhash
        self._total_thread_count = total_threads

        # The range of numbers to bruteforce from the hash generator
        self._start = start
        self._end = end

    def run(self):  # brute forces the hash
        tmp_end = self._start
        jump = self._jobs_per_thread(self._end - self._start)
        print(f"Starting to bruteforce: {self._myhash}")
        for _ in range(self._total_thread_count - 1):
            if tmp_end + jump < self._end:
                tmp_end += jump

            myThread(self._brute_force, args=(self._start, tmp_end)).start()
            self._start = tmp_end

        myThread(self._brute_force, args=(self._start, self._end)).start()

    def _brute_force(self, start, end):
        products = self._gen_bf(start, end)
        for plain_try in products:
            if not self._myhash.is_cracked:
                hashed_try = md5(plain_try.encode())
                hashed_try = hashed_try.hexdigest()
                if hashed_try == self._myhash.hash:
                    data = f"{self._myhash.hash}:{plain_try}"
                    self._myhash.plain_text = data



    # creating a generator for the brute forcing
    def _gen_bf(self, start, end):
        _iter = (str(i) for i in range(start, end + 1))
        for num in _iter:
            num = '0' * (self._myhash.length - len(num)) + num
            yield num

    # Class static methods:
    def _jobs_per_thread(self, range):
        return int(range / self._total_thread_count)

    # class properties
    @property
    def total_thread_count(self):
        return self._total_thread_count

    @total_thread_count.setter
    def total_thread_count(self, new_thread_count):
        self._total_thread_count = new_thread_count

    @property
    def myhash(self):
        return self._myhash

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, new_end):
        self._end = new_end

    @start.setter
    def start(self, new_start):
        self._start = new_start
