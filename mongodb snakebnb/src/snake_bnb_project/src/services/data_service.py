from data.owners import Owners
from data.cages import Cage
from typing import List


def create_account(name: str, email: str) -> Owners:
    owner = Owners()
    owner.name = name
    owner.email = email
    owner.save()
    return owner


def find_account_by_email(email: str) -> Owners:
    owner = Owners.objects().filter(email=email).first()
    return owner


def register_cage_host(active_account: Owners, client: str, meters, carpeted, toys, dangerous_snake) -> Cage:
    cage = Cage()
    cage.name = client
    cage.square_meters = meters
    cage.is_carpeted = carpeted
    cage.has_toys = toys
    cage.allow_dangerous_snakes = dangerous_snake
    cage.save()

    account = find_account_by_email(active_account.email)
    account.cage_ids.append(cage.id)
    account.save()

    return cage


def get_cages(active_account: Owners) -> List[Cage]:
    query = Cage.objects(id__in=active_account.cage_ids)
    cages = list(query)
    return cages
