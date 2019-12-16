from os import listdir
from os.path import isdir, dirname, join
from sys import stdout
from time import time as time

from helper import DownloadFailedError

AUTOMATIC = False


def custom_print(*data, new_line=True):
    if not AUTOMATIC:
        stdout.write(", ".join((str(x) for x in data)))
        if new_line:
            stdout.write("\n")
    pass


if __name__ == "__main__":
    direct = dirname(__file__)
    for fold in sorted(x for x in listdir(direct) if isdir(join(direct, x)) if str(x).startswith("Day16")):
        try:
            # noinspection PyUnresolvedReferences
            tmp = __import__("%s.task" % fold).task
            print('-' * 50)
            print(fold)
            custom_print('-' * 4)
            start_time = time()
            tmp.main(printer=custom_print)
            end_time = time()
            print('=' * 4)
            print("Time", "{time:10.3f}ms".format(time=(end_time - start_time) * 1000))
        except (AttributeError, ModuleNotFoundError, DownloadFailedError) as e:
            pass
