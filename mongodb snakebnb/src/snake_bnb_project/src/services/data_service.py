from data.owners import Owners


def create_account(name: str, email: str) -> Owners:
    owner = Owners()
    owner.name = name
    owner.email = email
    owner.save()
    return owner
