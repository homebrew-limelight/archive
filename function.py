from abc import ABC, abstractmethod
from dataclasses import is_dataclass, fields
from typing import Iterable, FrozenSet


def is_pydantic_dataclass(cls):
    return is_dataclass(cls) and hasattr(cls, "__pydantic_model__")


def does_match(cls, name, asserter):
    item = getattr(cls, name, None)
    return asserter(item)


class Function(ABC):
    has_sideeffect: bool
    require_restart: FrozenSet[str]

    def __init_subclass__(cls, require_restart: Iterable[str] = None, has_sideeffect: bool = False, **kwargs):
        super().__init_subclass__(**kwargs)

        cls.has_sideeffect = has_sideeffect

        if not does_match(cls, "Settings", is_pydantic_dataclass):
            raise TypeError(f"Class {cls.__name__} must have a pydantic dataclass 'Settings'")

        if not does_match(cls, "Inputs", is_dataclass):
            raise TypeError(f"Class {cls.__name__} must have a dataclass 'Inputs'")

        if not does_match(cls, "Outputs", is_dataclass):
            raise TypeError(f"Class {cls.__name__} must have a dataclass 'Outputs'")

        cls.require_restart = frozenset() if require_restart is None else frozenset(require_restart)

        for field in cls.require_restart:
            if field not in fields(cls.Settings):
                raise TypeError(f"Class {cls.__name__}.Settings must have a field '{field}'")

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

