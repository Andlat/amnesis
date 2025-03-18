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
@clipy.Command(
    name="models",
    usage="amnesis models",
    description="List all models",
    subcommands=[
        clipy.Command(
            name="delete",
            usage="amnesis models delete [model_name]",
            description="Delete a model",
            options=[clipy.Option(name="model_name", positional=True, type=str)],
        ),
    ],
)
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
    subcommands=[
        clipy.Command(
            name="delete",
            usage="amnesis experiments delete [uuid]",
            description="Delete an experiment by uuid",
            options=[clipy.Option(name="experiment uuid", positional=True, type=str)],
        ),
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
        subcommand_name = command.options['models']
        if subcommand_name == 'delete':
            try:
                repository.remove_model(model_name=options["model_name"])
                print(f'\033[92m{options["model_name"]} successfully deleted\033[0m\n')
            except Exception as e:
                print(f'\033[93m{e}\033[0m\n')

        list_models(repo=repository)

    elif command_name == "experiments":
        subcommand_name = command.options['experiments']
        if subcommand_name  == 'delete':
            try:
                repository.remove_experiment(experiment_uuid=options["experiment uuid"])
                print(f'\033[92m{options["experiment uuid"]} successfully deleted\033[0m\n')
            except Exception as e:
                print(f'\033[93m{e}\033[0m\n')

        list_experiments(
            repo=repository,
            model_name=options["model"],
            hyperparameters=options["hyperparameters"],
            metrics=options["metrics"],
            sort=options["sort"],
        )
    else:
        print(f"Unknown command: {command_name}")
