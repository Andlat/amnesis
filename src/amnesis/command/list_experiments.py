from amnesis.experiment import Experiment
from amnesis.repository import Repository


def get_model_names(repo: Repository):
    try:
        models = repo.get_models()
    except FileNotFoundError as error:
        print(error)

    return [model.name for model in models]


def print_experiment(
    experiment: Experiment,
    model_len=32,
    exp_len=32,
    date_len=32,
    uuid_len=32,
    highlight: bool = False,
):
    print(
        " * " if highlight else "   ",
        f"{experiment.model_name:<{model_len}}",
        f"{experiment.name:<{exp_len}}",
        f"{experiment.date:<{date_len}}",
        f"{experiment.uuid:<{uuid_len}}",
        sep="",
    )


def print_experiments(experiments, model_len=32, exp_len=32, date_len=32, uuid_len=32):
    # sort experiments by date
    experiments = sorted(experiments, key=lambda x: x.date, reverse=True)

    print(  # Header
        "   ",
        f"{'Model':<{model_len}}",
        f"{'Experiment':<{exp_len}}",
        f"{'Date':<{date_len}}",
        f"{'UUID':<{uuid_len}}",
        sep="",
    )

    print_experiment(
        experiments[0], model_len, exp_len, date_len, uuid_len, highlight=True
    )
    for experiment in experiments[1:]:
        print_experiment(experiment, model_len, exp_len, date_len, uuid_len)


def print_details_experiment(
    experiment: Experiment,
    hyperparameters,
    metrics,
    model_len=32,
    exp_len=32,
    max_hyper_len=32,
    max_metric_len=32,
    highlight: bool = False,
):
    line = " * " if highlight else "   "
    name = f"{experiment.model_name}/{experiment.name}"
    line += f"{name:<{model_len + exp_len + 1}}"

    for hyper in hyperparameters:
        line += f"{experiment.hyperparameters[hyper]:<{max_hyper_len}}"

    for metric in metrics:
        line += f"{experiment.metrics[metric]:<{max_metric_len}}"

    print(line)


def print_comparaison(experiments, model_len=32, exp_len=32, date_len=32, uuid_len=32):
    # sort experiments by date
    experiments = sorted(experiments, key=lambda x: x.date, reverse=True)

    hyperparameters = experiments[0].hyperparameters.keys()
    metrics = experiments[0].metrics.keys()

    max_hyper_len = max([len(hyper) for hyper in hyperparameters]) + 4
    max_metric_len = max([len(metric) for metric in metrics]) + 4

    header = "   "
    header += f"{'Model/Experiment':<{model_len + exp_len + 1}}"

    for hyper in hyperparameters:
        header += f"{hyper:<{max_hyper_len}}"

    for metric in metrics:
        header += f"{metric:<{max_metric_len}}"

    # f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

    print(header)
    print_details_experiment(
        experiments[0],
        hyperparameters,
        metrics,
        model_len,
        exp_len,
        max_hyper_len,
        max_metric_len,
        highlight=True,
    )
    for experiment in experiments[1:]:
        print_details_experiment(
            experiment,
            hyperparameters,
            metrics,
            model_len,
            exp_len,
            max_hyper_len,
            max_metric_len,
        )


def list_experiments(repo: Repository, model_name: str = None, compare: bool = False):
    models_name = get_model_names(repo)

    models = [model_name] if model_name in models_name else models_name

    experiments = []
    for model in models:
        experiments += repo.get_experiments(model)

    model_len = max([len(model) for model in models]) + 4
    exp_len = max([len(experiment.name) for experiment in experiments]) + 4
    date_len = 32
    uuid_len = 32

    if compare:
        print_comparaison(experiments, model_len, exp_len, date_len, uuid_len)
    else:
        print_experiments(experiments, model_len, exp_len, date_len, uuid_len)
