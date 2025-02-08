import clipy


@clipy.App(usage="amnesis [OPTIONS] COMMAND [ARGS] ...", description="A local experiments tracking tool")
@clipy.Command(name="init", usage="amnesis init", description="Initialize a new amnesis project")
@clipy.Command(name="info", usage="amnesis info", description="Show information about the current project")
@clipy.Command(name="models", usage="amnesis models", description="List all models")
@clipy.Command(name="experiments", usage="amnesis experiments", description="List all experiments")
def main(command: clipy.CommandDefinition):
    command_name = command.name

    if command_name == "init":
        print("Initializing a new amnesis project")
    elif command_name == "info":
        print("Showing information about the current project")
    elif command_name == "models":
        print("Listing all models")
    elif command_name == "experiments":
        print("Listing all experiments")
    else:
        print(f"Unknown command: {command_name}")
