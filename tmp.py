class Meta(type):

    def __getattr__(self, item):
        print(item)
        return item

class Tmp(metaclass=Meta):
    pass

Tmp.asdf