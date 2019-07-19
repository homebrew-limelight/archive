from abc import ABC, abstractmethod
from dataclasses import is_dataclass, dataclass, fields
from typing import FrozenSet

import pydantic
from pydantic import BaseModel

def does_match(cls, name, asserter, ignore_typeerorr: bool = True):
    if ignore_typeerorr:
        item = getattr(cls, name, None)
    else:
        item = getattr(cls, name, None)

    return asserter(item)


class Function(ABC):
    has_sideeffect: bool = True
    require_restart: FrozenSet[str] = frozenset()

    @pydantic.dataclasses.dataclass()
    class Settings(BaseModel):
        pass

    @dataclass
    class Inputs:
        pass

    @dataclass
    class Outputs:
        pass

    def __init_subclass__(cls, *args, **kwargs):
        def error(msg):
            raise TypeError(f"Function {cls.__name__} must have a {msg}")

        try:
            if not does_match(cls, "Settings", is_dataclass):
                error("dataclass 'Settings'")
        except AttributeError:
            cls.Settings = Function.Settings

        try:
            if not does_match(cls, "Inputs", is_dataclass):
                error("dataclass 'Inputs'")
        except AttributeError:
            cls.Inputs = Function.Inputs

        try:
            if not does_match(cls, "Outputs", is_dataclass):
                error("dataclass 'Outputs'")
        except AttributeError:
            cls.Outputs = Function.Outputs

        if not does_match(cls, "has_sideeffect", lambda x: isinstance(x, bool), ignore_typeerorr=False):
            error("bool property 'has_sideeffect'")

        if not hasattr(cls, "require_restart"):
            error("property 'require_restart'")

        cls.require_restart = frozenset(cls.require_restart)

        setting_names = [x.name for x in fields(cls.Settings)]

        for field in cls.require_restart:
            if field not in setting_names:
                error(f"field '{field}'")

    def __init__(self, settings):
        self.settings = settings

    @abstractmethod
    def __call__(self, inputs):
        raise NotImplementedError

    def dispose(self):
        pass

