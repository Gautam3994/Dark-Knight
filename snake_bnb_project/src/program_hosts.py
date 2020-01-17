from colorama import Fore
from infrastructure.switchlang import switch
import infrastructure.state as state
from services import data_service
import dateutil, datetime


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_cages)
            s.case('r', register_cage)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('Login to your [a]ccount')
    print('[L]ist your cages')
    print('[R]egister a cage')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')
    name = input("What is your name?")
    email = input("What is your mail id?").strip().lower()
    old_account = data_service.find_account_by_email(email)
    if old_account:
        error_msg(f"The account with the mail id {email} already exists")
        return
    state.active_account = data_service.create_account(name, email)
    print("The account was successfully created")


def log_into_account():
    print(' ****************** LOGIN **************** ')
    email = input("Enter your mail id?").strip().lower()
    login_mail = data_service.find_account_by_email(email)
    if not login_mail:
        error_msg("This email is not registered with any account.")
        return
    state.active_account = login_mail
    print("You have logged in successfully")


def register_cage():
    print(' ****************** REGISTER CAGE **************** ')
    if not state.active_account:
        error_msg("You must require an account to regsiter")
        return
    while True:
        meters = input("Length of the cage required?")
        if not meters:
            error_msg("This is a required field")
        else:
            try:
                length = float(meters)
            except:
                error_msg("You must enter numbers only")
            else:
                break
    carpeted = input("Is it carpeted [y, n]?").lower().startswith('y')
    toys = input("It has toys [y, n]?").lower().startswith('y')
    dangerous_snake = input("Is it a venomous snake [y, n]?").lower().startswith('y')
    client = input("Who is getting this cage?")
    cage = data_service.register_cage_host(state.active_account, client, length, carpeted, toys, dangerous_snake)
    state.reload_account()
    success_msg(f"Registerd cage with id{cage.id}")


def list_cages(supress_header=False):
    if not supress_header:
        print(' ******************     Your cages     **************** ')
    if not state.active_account:
        error_msg("You must login to find the list of cages")
        return
    your_cages = data_service.get_cages(state.active_account)
    print(f"You have {len(your_cages)} cages registered")
    for cage_no, cage in enumerate(your_cages):
        print(f"{cage_no + 1}- The {cage.name} is {cage.square_meters} meters")
        for booking in cage.bookings:
            print(f"Booking: {booking.check_in_date}, {(booking.check_out_date - booking.check_in_date).days}, "
                  f"booked{'Yes' if booking.booked_date is not None else 'No'} ")


def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg("You must login to add the availability of your cages")
        return
    while True:
        list_cages(supress_header=False)
        cage_to_check = input("Enter the number of the cage which you wanna update")
        if not cage_to_check:
            print("Please enter the suitable number")
        else:
            try:
                cage_number = int(cage_to_check)
            except:
                print("Please enter the suitable number")
            else:
                break
    cages = data_service.get_cages(state.active_account)
    selected_cage = cages[cage_number - 1]
    success_msg(f"You have selected the cage {selected_cage.name}")
    start_date = dateutil.parser.parse(input("Enter an available start date [yyyy-mm-dd]"))
    no_of_days_required = int(input("Enter the number of days you want to make it available"))
    data_service.add_availability(selected_cage, start_date, no_of_days_required)
    success_msg(
        f"The {selected_cage.name} has been marked available for {no_of_days_required} days starting from {start_date}")


def view_bookings():
    print(' ****************** Your bookings **************** ')
    if not state.active_account:
        error_msg("You must login to add the availability of your cages")
        return
    your_cages = data_service.get_cages(state.active_account)
    bookings = [(cage, booking) for cage in your_cages for booking in cage.bookings if booking.booked_date is not None]
    for cage, booking in bookings:
        print(" * Cage : {}, booked date: {}, from {} for {} days".format(cage.name,
                                                                          datetime.date(booking.booked_date.year,
                                                                                        booking.booked_date.month,
                                                                                        booking.booked_date.day),
                                                                          datetime.date(booking.check_in_date.year,
                                                                                        booking.check_in_date.month,
                                                                                        booking.check_in_date.day),
                                                                          (booking.check_out_date - booking.check_in_date).days
                                                                          ))


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
