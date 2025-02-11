from django.db import models


# Create your models here.
class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100,
    )

    