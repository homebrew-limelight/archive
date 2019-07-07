from typing import Dict, Type, Any

from function import Function


def fullname(cls: type) -> str:

    module = cls.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return cls.__qualname__
    else:
        return module + '.' + cls.__qualname__


class Manager:
    idDict: Dict[str, Type[Function]]

    def __init__(self):
        self.idDict = {}

    def register(self, cls: Type[Function]) -> None:
        self.idDict[fullname(cls)] = cls

    def create(self, name: str, settings) -> Function:
        return self.idDict[name](settings)


