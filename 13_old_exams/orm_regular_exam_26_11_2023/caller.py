import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft


# Create queries within functions
def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    astronauts = Astronaut.objects.filter(query).order_by('name')

    if not astronauts:
        return ''

    result = []
    for a in astronauts:
        result.append(
            f"Astronaut: {a.name}, phone number: {a.phone_number}, "
            f"status: {'Active' if a.is_active else 'Inactive'}"
        )

    return '\n'.join(result)


def get_top_astronaut():
    top = Astronaut.objects.prefetch_related(
        'missions'
    ).annotate(
        missions_count=Count('missions')
    ).order_by(
        '-missions_count', 'phone_number'
    ).first()

    if not Mission.objects.all() or not Astronaut.objects.all():
        return "No data."
    return f"Top Astronaut: {top.name} with {top.missions_count} missions."


def get_top_commander():
    top_commander = Astronaut.objects.annotate(
        missions_count=Count('commanded_missions')
    ).order_by(
        '-missions_count', 'phone_number'
    ).first()

    if not top_commander or top_commander.missions_count == 0:
        return "No data."
    return f"Top Commander: {top_commander.name} with {top_commander.missions_count} commanded missions."


# ------------------------------------------------------------------------------------------
def get_last_completed_mission():
    mission = Mission.objects.filter(
        status='Completed'
    ).order_by(
        '-launch_date'
    ).first()

    if not mission:
        return "No data."

    return (f"The last completed mission is: {mission.name}. "
            f"Commander: {'TBA' if not mission.commander else mission.commander.name}. "
            f"Astronauts: {', '.join([a.name for a in mission.astronauts.all().order_by('name')])}. "
            f"Spacecraft: {mission.spacecraft.name}. "
            f"Total spacewalks: {sum([a.spacewalks for a in mission.astronauts.all()])}.")


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(
        missions_count=Count('used_in_missions')
    ).order_by(
        'name'
    ).first()

    if not spacecraft or spacecraft.missions_count == 0:
        return "No data."

    unique_astronauts = set()
    missions_with_spacecraft = Mission.objects.filter(spacecraft=spacecraft)

    for m in missions_with_spacecraft:
        for a in m.astronauts.all():
            unique_astronauts.add(a.id)

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.missions_count} missions, "
            f"astronauts on missions: {len(unique_astronauts)}.")


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(
        used_in_missions__status='Planned', weight__gte=200.0
    ).distinct()

    if not spacecrafts:
        return "No changes in weight."

    for s in spacecrafts:
        s.weight = s.weight - 200
        s.save()

    all_spacecrafts = Spacecraft.objects.all()
    avg_weight = sum([s.weight for s in all_spacecrafts]) / len(all_spacecrafts)

    return (f"The weight of {len(spacecrafts)} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")

