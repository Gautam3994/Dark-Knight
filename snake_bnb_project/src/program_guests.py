from infrastructure.switchlang import switch
import program_hosts as hosts
from program_hosts import error_msg, success_msg
import infrastructure.state as state
from services import data_service
from dateutil import parser
import datetime


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
    length = int(input("what is the length of the snake in meters"))
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
    if not state.active_account:
        error_msg("You must login in order to add a snake")
        return
    your_snakes = data_service.get_your_snake(state.active_account)
    if not your_snakes:
        error_msg("You don't have snake registered. Please [a]dd")
        return
    while True:
        while True:
            start_date_text = input("Enter the date in which you want to book the cage [yyyy-mm-dd]:")
            if not start_date_text:
                error_msg("Please enter start date")
            else:
                break
        while True:
            end_date_text = input("Enter the date in which you want to end the booking of the cage [yyyy-mm-dd]:")
            if not end_date_text:
                error_msg("Please enter end date")
            else:
                break
        check_in = parser.parse(start_date_text)
        check_out = parser.parse(end_date_text)
        if check_in >= check_out:
            error_msg("Check in date must before check out date")
        else:
            break
    print()
    for no, snake in enumerate(your_snakes):
        print(f"{no + 1} - The snake {snake.name} is {snake.length} meter(s) long and is {'venomous'if snake.is_venomous else ''}")
    snake_picked = your_snakes[int(input("Choose the number of the snake for which you are lookinf for a cage")) - 1]
    cages = data_service.get_available_cages(check_in, check_out, snake_picked)
    print(f"There are {len(cages)} cages available")
    if len(cages) == 0:
        print("Sorry there are no cages available")
        return
    for cage_no, cage in enumerate(cages):
        print(f"{cage_no + 1} - {cage.name} which is {cage.square_meters} meters long. Carpeted: {'yes' if cage.is_carpeted else 'no'}  Has Toys: {'yes' if cage.has_toys else 'no'}")
    selected_cage = cages[int(input("Please choose the number of any available cage")) - 1]
    data_service.book_cage(state.active_account, selected_cage, snake_picked, check_in, check_out)
    success_msg(f"You have successuly booked {selected_cage.name} from {check_in} to {check_out} for {snake_picked}")


def view_bookings():
    print(' ****************** Your bookings **************** ')
    if not state.active_account:
        error_msg("You must login in order to add a snake")
        return
    your_snakes = {snake.id: snake for snake in data_service.get_your_snake(state.active_account)}
    bookings = data_service.get_your_bookings(state.active_account)
    print(f"You have {len(bookings)} bookings")
    for b in bookings:
        print("* Snake: {} is booked at {} from {} for {} days".format(your_snakes.get(b.guest_snake_id).name, b.cage.name,
                                                                       datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
                                                                       (b.check_out_date - b.check_in_date).days))
    # Easier Method but slow find below
    # your_snakes = data_service.get_your_snake(state.active_account)
    # for snake in your_snakes:
    #     your_bookings = data_service.get_your_bookings(state.active_account, snake.id)




