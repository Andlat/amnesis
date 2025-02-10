import clipy

from .repository import Repository


def init():
    repository = Repository()

    try:
        repository.init()
        print("Amnesis repository initialized")
    except FileExistsError:
        print("Repository is already initialized")


def list_models():
    repository = Repository()

    try:
        models = repository.get_models()
    except FileNotFoundError as error:
        print(error)

    print("Model")
    for model in models:
        print(model.name)


def list_experiments(model_name: str = None):
    repository = Repository()

    try:
        models = repository.get_models()
        models_name = [model.name for model in models]

        models = [model_name] if model_name in models_name else models_name

        experiments = []
        for model in models:
            experiments += repository.get_experiments(model)
    except FileNotFoundError as error:
        print(error)

    # sort experiments by date
    experiments = sorted(experiments, key=lambda x: x.date, reverse=True)

    max_model_name_length = max([len(model) for model in models]) + 8
    max_experiment_name_length = max([len(experiment.name) for experiment in experiments]) + 8
    date_char_length = 32
    uuid_char_length = 32

    print(
        "   ",
        f"{'Model':<{max_model_name_length}}",
        f"{'Experiment':<{max_experiment_name_length}}",
        f"{'Date':<{date_char_length}}",
        f"{'UUID':<{uuid_char_length}}",
        sep=""
    )
    print(
        " * ", # highlight the latest experiment
        f"{experiments[0].model_name:<{max_model_name_length}}",
        f"{experiments[0].name:<{max_experiment_name_length}}",
        f"{experiments[0].date:<{date_char_length}}",
        f"{experiments[0].uuid:<{uuid_char_length}}",
        sep=""
    )
    for experiment in experiments[1:]:
        print(
            "   ",
            f"{experiment.model_name:<{max_model_name_length}}",
            f"{experiment.name:<{max_experiment_name_length}}",
            f"{experiment.date:<{date_char_length}}",
            f"{experiment.uuid:<{uuid_char_length}}",
            sep=""
        )


@clipy.App(usage="amnesis [OPTIONS] COMMAND [ARGS] ...", description="A local experiments tracking tool")
@clipy.Command(name="init", usage="amnesis init", description="Initialize a new amnesis project")
@clipy.Command(name="info", usage="amnesis info", description="Show information about the current project")
@clipy.Command(name="models", usage="amnesis models", description="List all models")
@clipy.Command(name="experiments", usage="amnesis experiments", description="List all experiments", options=[
    clipy.Option(name="model", type=str, default=None, required=False)
])
def main(command: clipy.CommandDefinition):
    command_name = command.name

    if command_name == "init":
        init()
    elif command_name == "info":
        print("Showing information about the current project")
    elif command_name == "models":
        list_models()
    elif command_name == "experiments":
        list_experiments(command.options["model"])
    else:
        print(f"Unknown command: {command_name}")
