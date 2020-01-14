from data.owners import Owners


def create_account(name: str, email: str) -> Owners:
    owner = Owners()
    owner.name = name
    owner.email = email
    owner.save()
    return owner


def find_account_by_email(email: str) -> Owners:
    owner = Owners.objects().filter(email=email).first()
    return owner
