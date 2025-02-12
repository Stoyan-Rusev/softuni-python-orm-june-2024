from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager
from main_app.mixins import AwardedUpdatedMixin


# Create your models here.
class BaseClass(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )
    birth_date = models.DateField(
        default='1900-01-01',
    )
    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )


class Director(BaseClass):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    def __str__(self):
        return self.full_name

    objects = DirectorManager()


class Actor(BaseClass, AwardedUpdatedMixin):
    def __str__(self):
        return self.full_name


class Movie(AwardedUpdatedMixin):
    class MovieChoices(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )
    release_date = models.DateField()
    storyline = models.TextField(
        null=True,
        blank=True,
    )
    genre = models.CharField(
        max_length=6,
        choices=MovieChoices.choices,
        default=MovieChoices.OTHER,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0
    )
    is_classic = models.BooleanField(
        default=False,
    )
    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='director_movies',
    )
    starring_actor = models.ForeignKey(
        to=Actor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='starring_actor_movies',
    )
    actors = models.ManyToManyField(
        to=Actor,
        related_name='actor_movies',
    )

    def __str__(self):
        return self.title
