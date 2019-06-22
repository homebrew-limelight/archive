from typing import Dict

from function import Function


class Manager:
    idDict: Dict[str, type[Function]]

    def __init__(self):
        self.idDict = {}

# TODO: Same name collision
    def register(self, clazz: type[Function]):
        self.idDict[clazz.__name__] = clazz

    def create(self, name: str, settings):
        return self.idDict[name](settings)


