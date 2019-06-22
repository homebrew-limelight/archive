from typing import Dict, Type

from function import Function


class Manager:
    idDict: Dict[str, Type[Function]]

    def __init__(self):
        self.idDict = {}

# TODO: Same name collision
    def register(self, clazz: Type[Function]):
        self.idDict[clazz.__name__] = clazz

    def create(self, name: str, settings):
        return self.idDict[name](settings)


