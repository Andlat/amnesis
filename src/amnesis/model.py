import abc
import pathlib


class ModelSerializer(abc.ABC):
    @abc.abstractmethod
    def save(self, model, path: pathlib.Path):
        pass

    @abc.abstractmethod
    def load(self, path: pathlib.Path):
        pass
