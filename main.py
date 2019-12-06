from os import listdir
from os.path import isdir, dirname, join

if __name__ == "__main__":
    direct = dirname(__file__)
    for fold in sorted(x for x in listdir(direct) if isdir(join(direct, x)) if x == "Day05"):
        try:
            # noinspection PyUnresolvedReferences
            tmp = __import__("%s.task" % fold).task
            print(fold)
            tmp.main()
        except (AttributeError, ModuleNotFoundError) as e:
            pass
