from threading import Thread
from Validators.validators import val_function
class MyThread:

    def __init__(self, target, args=()):
        val_function(target=target)

        self._target = target
        self._args = args

    def start(self):
        """
        starting the thread
        :return:
        """
        Thread(target=self._target, args=self._args).start()
