import clipy

from amnesis.repository import Repository

from .initialization import init
from .list_experiments import list_experiments
from .list_models import list_models


@clipy.App(
    usage="amnesis [OPTIONS] COMMAND [ARGS] ...",
    description="A local experiments tracking tool",
)
@clipy.Command(
    name="init", usage="amnesis init", description="Initialize a new amnesis project"
)
@clipy.Command(
    name="info",
    usage="amnesis info",
    description="Show information about the current project",
)
@clipy.Command(name="models", usage="amnesis models", description="List all models")
@clipy.Command(
    name="experiments",
    usage="amnesis experiments",
    description="List all experiments",
    options=[
        clipy.Option(name="model", type=str, default=None, required=False),
        clipy.Option(
            name="hyperparameters", action="store_true", default=False, required=False
        ),
        clipy.Option(
            name="metrics", action="store_true", default=False, required=False
        ),
        clipy.Option(name="sort", type=str, default=None, required=False),
    ],
)
def main(command: clipy.CommandDefinition):
    command_name = command.name
    options = command.options

    repository = Repository()
    in_repository = repository.in_repository()

    if not in_repository and command_name != "init":
        print(
            "Not in an amnesis repository. Run `amnesis init` to initialize a new repository."
        )
        return

    if command_name == "init":
        init(repo=repository)
    elif command_name == "info":
        raise NotImplementedError
    elif command_name == "models":
        list_models(repo=repository)
    elif command_name == "experiments":
        list_experiments(
            repo=repository,
            model_name=options["model"],
            hyperparameters=options["hyperparameters"],
            metrics=options["metrics"],
            sort=options["sort"],
        )
    else:
        print(f"Unknown command: {command_name}")
