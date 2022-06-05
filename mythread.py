from threading import Thread

class MyThread:

    def __init__(self, target, args=()):
        self._target = target
        self._args = args

    #starting the threads:
    def start(self):
        Thread(target=self._target, args=self._args).start()

    @staticmethod
    def jobs_per_thread(jobs, threads):
        return int(jobs / threads)
