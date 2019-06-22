from typing import Dict

from function import Function


class Manager:
    idDict: Dict[str, type]

    def __init__(self):
        self.idDict = {}

# TODO: Same name collision
    def register(self, clazz: type):
        self.idDict[clazz.__name__] = clazz

    def create(self, name: str, settings):
        return self.idDict[name](settings)


m = Manager()
m.register(Function)
z = m.create("Function", 1)
print(getattr(z, "settings"))
