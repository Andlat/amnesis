import dataclasses
import json
import pathlib


@dataclasses.dataclass(order=True)
class Experiment:
    git: str

    model_name: str
    name: str
    uuid: str

    date: str
    time: float
    hyperparameters: dict
    metrics: dict

    def save(self, path: pathlib.Path):
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w") as file:
            json.dump(dataclasses.asdict(self), file, indent=4)

    @classmethod
    def load(cls, path: pathlib.Path):
        with path.open() as file:
            metadata = json.load(file)

        return cls(**metadata)
