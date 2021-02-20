class TMP:

    def __getattr__(self, item):
        return lambda: print(item)


TMP().a()