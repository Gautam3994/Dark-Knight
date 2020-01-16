from infrastructure.switchlang import switch
import program_hosts as hosts
from program_hosts import error_msg, success_msg
import infrastructure.state as state
from services import data_service


def run():
    print(' ****************** Welcome guest **************** ')
    print()

    show_commands()

    while True:
        action = hosts.get_action()

        with switch(action) as s:
            s.case('c', hosts.create_account)
            s.case('l', hosts.log_into_account)

            s.case('a', add_a_snake)
            s.case('y', view_your_snakes)
            s.case('b', book_a_cage)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')

            s.case('?', show_commands)
            s.case('', lambda: None)
            s.case(['x', 'bye', 'exit', 'exit()'], hosts.exit_app)

            s.default(hosts.unknown_command)

        state.reload_account()

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[B]ook a cage')
    print('[A]dd a snake')
    print('View [y]our snakes')
    print('[V]iew your bookings')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def add_a_snake():
    print(' ****************** Add a snake **************** ')
    if not state.active_account:
        error_msg("You must login in order to add a snake")
        return
    while True:
        name = input("What is the name for your snake")
        if not name:
            error_msg("This is a required field")
        else:
            break
    length = float(input("what is the length of the snake in meters"))
    is_venomous = input("Is your snake venomous [y]es or [n]o").lower().startswith('y')
    species = input("What species is your snake?")
    snake = data_service.add_snake(state.active_account, name, length, is_venomous, species)
    state.reload_account()
    success_msg(f"Your snake {snake.name} has added successfully")


def view_your_snakes():
    print(' ****************** Your snakes **************** ')
    if not state.active_account:
        error_msg("You must login in order to add a snake")
        return
    your_snakes = data_service.get_your_snake(state.active_account)
    print(f"You have {len(your_snakes)} snakes")
    for snake in your_snakes:
        print(f"Your snake {snake.name} is {snake.length} meters long and is {'' if snake.is_venomous else 'not'} venomous")


def book_a_cage():
    print(' ****************** Book a cage **************** ')
    # TODO: Require an account
    # TODO: Verify they have a snake
    # TODO: Get dates and select snake
    # TODO: Find cages available across date range
    # TODO: Let user select cage to book.

    print(" -------- NOT IMPLEMENTED -------- ")


def view_bookings():
    print(' ****************** Your bookings **************** ')
    # TODO: Require an account
    # TODO: List booking info along with snake info

    print(" -------- NOT IMPLEMENTED -------- ")
