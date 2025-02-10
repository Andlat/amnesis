import time

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

        experiment.log_metric("metric1", 0.95)
        experiment.log_metric("metric2", 0.75)

        experiment.log_model(model, serializer=NumpySerializer())


if __name__ == "__main__":
    main()
