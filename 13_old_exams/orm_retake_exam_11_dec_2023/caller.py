import os
import django
from django.db.models import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None):
    players = []

    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(
            full_name__icontains=search_name,
            country__icontains=search_country,
        ).order_by(
            'ranking'
        )

    elif search_name is not None:
        players = TennisPlayer.objects.filter(
            full_name__icontains=search_name
        ).order_by(
            'ranking'
        )

    elif search_country is not None:
        players = TennisPlayer.objects.filter(
            country__icontains=search_country
        ).order_by(
            'ranking'
        )

    else:
        return ''
    return '\n'.join([f'Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}' for p in players])


def get_top_tennis_player():
    top_player = TennisPlayer.objects.annotate(
        wins=Count('winner_match')
    ).order_by(
        '-wins', 'full_name'
    ).first()

    if not top_player:
        return ''
    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins} wins."


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(
        matches_played=Count(
            'player_matches'
        )
    ).order_by(
        '-matches_played', 'ranking'
    ).first()

    if not player or not player.matches_played:
        return ''
    return f"Tennis Player: {player.full_name} with {player.matches_played} matches played."


# ------------------------------------------------------------------------------

def get_tournaments_by_surface_type(surface=None):
    tournaments = Tournament.objects.annotate(
        num_matches=Count('tournament_matches')
    ).filter(
        surface_type__icontains=surface,
    ).order_by(
        '-start_date'
    )

    if not tournaments or surface is None:
        return ''

    return '\n'.join([f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}" for t in tournaments])

# Моето решение:
def get_latest_match_info():
    latest_match = Match.objects \
        .prefetch_related('players') \
        .order_by('-date_played', '-id') \
        .first()

    if latest_match is None:
        return ''

    players = latest_match.players.order_by('full_name')

    players_names = [p.full_name for p in players]
    winner = latest_match.winner

    return (f"Latest match played on: {latest_match.date_played}, "
            f"tournament: {latest_match.tournament.name}, "
            f"score: {latest_match.score}, players: {' vs '.join(players_names)}, "
            f"winner: {'TBA' if winner is None else winner.full_name}, "
            f"summary: {latest_match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return 'No matches found'

    matches = Match.objects.filter(tournament__name=tournament_name).order_by('-date_played')
    if not matches:
        return 'No matches found'

    result = []
    for m in matches:
        result.append(f"Match played on: {m.date_played}, "
                      f"score: {m.score}, "
                      f"winner: {'TBA' if not m.winner else m.winner.full_name}")
    return '\n'.join(result)


# print(get_latest_match_info())
