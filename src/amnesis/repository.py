import os
import pathlib

from .experiment import Experiment


class Repository:
    def __init__(self):
        self.root = None
        self.dir_name = ".amnesis"

    def init(self, path: pathlib.Path = None):
        if path is None:
            path = pathlib.Path.cwd()

        repository_dir = path / self.dir_name

        if repository_dir.exists():
            raise FileExistsError(f"Repository already exists in {path}")

        self.root = path
        repository_dir.mkdir(parents=True, exist_ok=True)

    def in_project(self):
        path = pathlib.Path.cwd()
        return self._get_root_path(path) is not None

    def get_root(self):
        path = pathlib.Path.cwd()
        return self._get_root_path(path)

    def get_amnesis_dir(self):
        if self.in_project():
            return self.get_root() / self.dir_name

        if self.root:
            return self.root / self.dir_name

        raise FileNotFoundError("Cannot find `.amnesis` directory")

    def get_models(self):
        amnesis_dir = self.get_amnesis_dir()
        # models = list(amnesis_dir.glob("*"))

        models = []
        for model in amnesis_dir.iterdir():
            if model.is_dir():
                models.append(model)

        if models:
            return models

        return None

    def get_experiments(self, model_name: str):
        models = self.get_models()

        if models is None:
            return None

        models_names = [model.name for model in models]

        if model_name not in models_names:
            return None

        experiments = []
        model_dir = self.get_amnesis_dir() / model_name

        for experiment in model_dir.iterdir():
            if experiment.is_dir():
                experiments.append(Experiment.load(experiment / "metadata.json"))

        return experiments

    def _get_root_path(self, path: pathlib.Path):
        if self.root:
            return self.root

        repository_dir = path / self.dir_name
        if repository_dir.exists():
            self.root = path
            return path

        path = path.parent
        if os.path.abspath(path) == os.path.abspath(os.sep):
            return None

        return self._get_root_path(path)
