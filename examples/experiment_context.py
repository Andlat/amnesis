import pathlib
import time

import matplotlib.pyplot as plt
import numpy

from amnesis import ExperimentContext, ModelSerializer


class NumpySerializer(ModelSerializer):
    def save(self, model, path):
        numpy.save(path, model)

    def load(self, path):
        return numpy.load(path)


def main():
    with ExperimentContext(model_name="model_name") as experiment:
        experiment.log_hyperparameter("hyper_param1", 0.01)
        experiment.log_hyperparameter("hyper_param2", 32)

        print("Running experiment...")

        # Mock experiment
        time.sleep(1)

        # Mock model
        model = numpy.random.rand(10, 10)

        # save sinusoide plot artifact
        x = numpy.linspace(0, 2 * numpy.pi, 100)
        y = numpy.sin(x)
        plt.plot(x, y)

        output_path = pathlib.Path("./output/sinusoide.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.savefig(str(output_path))
        experiment.log_artifact(output_path)

        # Save a folder as artifact
        folder_path = pathlib.Path("./output/folder")
        subfolder_path = folder_path / "subfolder"
        subfolder_path.mkdir(parents=True, exist_ok=True)

        with open(folder_path / "file1.txt", "w", encoding="utf8") as f:
            f.write("Hello, World!")

        with open(subfolder_path / "file2.txt", "w", encoding="utf8") as f:
            f.write("Hello, World!")

        experiment.log_artifact(folder_path)

        experiment.log_metric("metric1", 0.95)
        experiment.log_metric("metric2", 0.75)

        experiment.log_model(model, serializer=NumpySerializer())


if __name__ == "__main__":
    main()
