import os
import django
import random
from datetime import datetime


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie
from django.db.models import Count, Q, F


def get_directors(search_name=None, search_nationality=None):
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is None and search_nationality is None:
        return ''

    elif search_name is not None and search_nationality is not None:
        query = query_name & query_nationality

    elif search_name is None and search_nationality is not None:
        query = query_nationality

    else:
        query = query_name

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []
    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}")
    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()
    if not top_director:
        return ''
    return f"Top Director: {top_director.full_name}, movies: {top_director.movie_count}."


def get_top_actor():
    top_actor = (Actor.objects.prefetch_related('starring_actor_movies')
                 .annotate(num_of_movies=Count('starring_actor_movies'))
                 .order_by('-num_of_movies', 'full_name').first())
    movies = Movie.objects.all()

    if not top_actor or not movies:
        return ''

    ratings_sum = sum([m.rating for m in top_actor.starring_actor_movies.all()])
    movies_count = len([m for m in top_actor.starring_actor_movies.all()])

    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {', '.join([m.title for m in top_actor.starring_actor_movies.all()])}, "
            f"movies average rating: "
            f"{ratings_sum / movies_count:.1f}")


def get_actors_by_movies_count():
    top_three = (Actor.objects.prefetch_related('actor_movies')
                 .annotate(movies_count=Count('actor_movies'))
                 .order_by('-movies_count', 'full_name'))[:3]
    if not top_three or not top_three[0].movies_count:
        return ''

    result = []
    for a in top_three:
        result.append(f"{a.full_name}, participated in {a.movies_count} movies")
    return '\n'.join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()
    if not movie:
        return ''

    starring_actor_name = 'N/A'
    actors = movie.actors.order_by('full_name')

    starring_actor = movie.starring_actor
    if starring_actor:
        starring_actor_name = starring_actor.full_name

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating:.1f}. Starring actor: {starring_actor_name}. "
            f"Cast: {', '.join([a.full_name for a in actors])}.")


def increase_rating():
    updated_movies_count = Movie.objects.filter(is_classic=True, rating__lt=10.0).update(rating=F('rating') + 0.1)
    if not updated_movies_count:
        return "No ratings increased."
    return f"Rating increased for {updated_movies_count} movies."

