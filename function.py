import abc


class Function(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def test():
        pass

    def __init__(self, settings):
        self.settings = settings

    @abc.abstractmethod
    def process(self, inputs, settings=None):
        pass


