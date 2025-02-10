from amnesis.repository import Repository


def init(repo: Repository):
    try:
        repo.init()
        print("Amnesis repository initialized")
    except FileExistsError:
        print("Repository is already initialized")
