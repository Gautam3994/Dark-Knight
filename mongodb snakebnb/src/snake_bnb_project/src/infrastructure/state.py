from data.owners import Owners
active_account: Owners = None


def reload_account():
    global active_account
    if not active_account:
        return

    # TODO: pull owner account from the database.
    pass

