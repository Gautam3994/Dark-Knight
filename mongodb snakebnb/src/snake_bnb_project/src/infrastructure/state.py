from data.owners import Owners
from services import data_service
active_account: Owners = None


def reload_account():
    global active_account
    if not active_account:
        return
    active_account = data_service.find_account_by_email(active_account.email)


