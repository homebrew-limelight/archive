from abc import ABC, abstractmethod
from dataclasses import is_dataclass
from typing import Iterable, TypeVar, Generic
import pydantic


def is_basemodel(cls):
    return isinstance(cls, type(pydantic.BaseModel))


def does_match(cls, name, asserter):
    item = getattr(cls, name, None)
    return asserter(item)


class Function(ABC):
    def __init_subclass__(cls, require_restart: Iterable[str] = None, has_sideeffect: bool = False, **kwargs):
        super().__init_subclass__(**kwargs)

        cls.has_sideeffect = has_sideeffect

        # if not does_match(cls, "Settings", is_basemodel):
        #     raise TypeError(f"Class {cls.__name__} must have a BaseModel 'Settings'")
        #
        # if not does_match(cls, "Inputs", is_dataclass):
        #     raise TypeError(f"Class {cls.__name__} must have a dataclass 'Inputs'")
        #
        # if not does_match(cls, "Outputs", is_dataclass):
        #     raise TypeError(f"Class {cls.__name__} must have a dataclass 'Outputs'")

        cls.require_restart = [] if require_restart is None else require_restart

        # TODO: TypeError for typos iun require_restart

    def __init__(self, settings):
        self.settings = settings

    def __call__(self, settings, inputs):
        if settings:
            self.settings = settings

        return self.process(inputs)

    @abstractmethod
    def process(self, inputs):
        raise NotImplementedError

