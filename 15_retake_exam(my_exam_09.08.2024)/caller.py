import os
from decimal import Decimal

import django
from django.db.models import Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import House, Dragon, Quest


# Create queries within functions
def get_houses(search_string=None):
    if search_string is None or search_string == "":
        return "No houses match your search."

    query = Q(name__istartswith=search_string) | Q(motto__istartswith=search_string)
    houses = House.objects.filter(
        query
    ).order_by(
        '-wins',
        'name'
    )

    if not houses.exists():
        return "No houses match your search."

    return '\n'.join([f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}" for h in houses])


def get_most_dangerous_house():
    most_dangerous = House.objects.get_houses_by_dragons_count().first()

    if not most_dangerous or most_dangerous.dragons_count == 0:
        return "No relevant data."

    return (f"The most dangerous house is the House of {most_dangerous.name} "
            f"with {most_dangerous.dragons_count} dragons. "
            f"Currently {'ruling' if most_dangerous.is_ruling else 'not ruling'} the kingdom.")


def get_most_powerful_dragon():
    most_powerful = Dragon.objects.filter(
        is_healthy=True
    ).order_by(
        '-power',
        'name'
    ).first()

    if not most_powerful:
        return "No relevant data."

    return (f"The most powerful healthy dragon is {most_powerful.name} "
            f"with a power level of {most_powerful.power:.1f}, "
            f"breath type {most_powerful.breath}, and {most_powerful.wins} wins, "
            f"coming from the house of {most_powerful.house.name}. "
            f"Currently participating in {most_powerful.dragon_quests.all().count()} quests.")


# ----------------------------------------------------------------------------------------------

def update_dragons_data():
    dragons = Dragon.objects.filter(
        is_healthy=False,
        power__gt=1.0
    ).order_by(
        'power'
    )

    if not dragons.exists():
        return "No changes in dragons data."

    for d in dragons:
        d.power -= Decimal('0.1')
        d.is_healthy = True
        d.save()

    all_dragons = Dragon.objects.all().order_by('power')

    return (f"The data for {dragons.count()} dragon/s has been changed. "
            f"The minimum power level among all dragons is {all_dragons.first().power:.1f}")


def get_earliest_quest():
    quest = Quest.objects.order_by(
        'start_time'
    ).first()

    if not quest:
        return "No relevant data."

    dragons = quest.dragons.all().order_by('-power', 'name')
    num_of_dragons = len(dragons)

    if num_of_dragons > 0:
        avg_power = sum(d.power for d in dragons) / num_of_dragons
    else:
        avg_power = 0

    return (f"The earliest quest is: {quest.name}, "
            f"code: {quest.code}, "
            f"start date: {quest.start_time.day}.{quest.start_time.month}.{quest.start_time.year}, "
            f"host: {quest.host.name}. Dragons: {'*'.join([d.name for d in dragons])}. "
            f"Average dragons power level: {avg_power:.2f}")


def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(
        code=quest_code
    ).first()

    if not quest:
        return "No such quest."

    winner = quest.dragons.order_by(
        '-power',
        'name'
    ).first()
    house = winner.house

    winner.wins += 1
    house.wins += 1
    house.save()
    winner.save()
    quest.delete()

    return (f"The quest: {quest.name} has been won by dragon {winner.name} from house {house.name}. "
            f"The number of wins has been updated as follows: {winner.wins} total wins for the dragon "
            f"and {house.wins} total wins for the house. The house was awarded with {quest.reward:.2f} coins.")
