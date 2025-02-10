from amnesis.repository import Repository


def list_models(repo: Repository):
    try:
        models = repo.get_models()
    except FileNotFoundError as error:
        print(error)

    print("Model")
    for model in models:
        print(model.name)
