from data.owners import Owners
from data.cages import Cage
from data.bookings import Booking
from data.snake_details import Snake
from typing import List
import datetime


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


def add_availability(account: Owners, selected_cage: Cage, start_date: datetime.datetime,
                     no_of_days_required: int) -> Cage:
    booking = Booking()
    booking.check_in_date = start_date
    booking.check_out_date = start_date + datetime.timedelta(no_of_days_required)
    cage = Cage.objects(id=selected_cage.id).first()
    cage.bookings.append(booking)
    cage.save()
    return cage


def add_snake(active_account: Owners, name: str, length: int, is_venomous: bool, species: str) -> Snake:
    snake = Snake()
    snake.name = name
    snake.length = length
    snake.is_venomous = is_venomous
    snake.species = species
    snake.save()

    account = find_account_by_email(active_account.email)
    account.snake_ids.append(snake.id)
    account.save()

    return snake


def get_your_snake(active_account: Owners) -> List[Snake]:
    snakes = Snake.objects(id__in=active_account.snake_ids).all()
    return list(snakes)


def get_available_cages(check_in: datetime.datetime, check_out: datetime.datetime, snake_picked: Snake) -> List[Cage]:
    min_size = snake_picked.length / 4
    cages = Cage.objects().filter(square_meters__gte=min_size).filter(bookings__check_in_date__lte=)
