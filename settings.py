from dataclasses import dataclass
import pickle


@dataclass
class Settings:
    number: int = 1


def dump_settings(settings: Settings) -> bytes:
    return pickle.dumps(settings)


def load_settings(data: bytes) -> Settings:
    return pickle.loads(data)
