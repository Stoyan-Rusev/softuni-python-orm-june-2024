import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


# Create queries within functions
def create_pet(name: str, species: str):
    pet = Pet.objects.create(
        name=name,
        species=species)

    return f"{pet.name} is a very cute {pet.species}!"


# print(create_pet('Rex', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    all_artifacts = Artifact.objects.all()
    all_artifacts.delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)


def show_all_locations():
    result = []
    locations = Location.objects.all().order_by('-id')
    for location in locations:
        result.append(f'{location.name} has a population of {location.population}!')
    return '\n'.join(result)


# print(show_all_locations())


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


# new_capital()


def delete_first_location():
    first_location = Location.objects.first()
    first_location.delete()


# delete_first_location()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


# print(get_capitals())


def apply_discount():
    all_cars = Car.objects.all()
    for car in all_cars:
        percentage_discount = sum(int(digit) for digit in str(car.year)) / 100
        car.price_with_discount = float(car.price) - float(car.price) * percentage_discount
    all_cars.bulk_update(all_cars, ['price_with_discount'])


# apply_discount()


def get_recent_cars():
    recent_cars = Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')
    return recent_cars


# print(get_recent_cars())


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    return '\n'.join([str(task) for task in Task.objects.all() if not task.is_finished])


# print(show_unfinished_tasks())


def complete_odd_tasks():
    tasks = Task.objects.all()
    for task in tasks:
        if task.id % 2 != 0:
            task.is_finished = True
    Task.objects.bulk_update(tasks, ['is_finished'])


# complete_odd_tasks()


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join([chr(ord(ch) - 3) for ch in text])

    Task.objects.filter(title=task_title).update(description=encoded_text)

    # tasks_to_encode = Task.objects.all().filter(title=task_title)
    #
    # for t in tasks_to_encode:
    #     t.description = encoded_text
    #
    # Task.objects.bulk_update(tasks_to_encode, ['description'])


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_deluxe_rooms = [str(r) for r in deluxe_rooms if r.id % 2 == 0]

    return '\n'.join(even_deluxe_rooms)


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()
    if not room.is_reserved:
        room.delete()
