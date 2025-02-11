# Generated by Django 5.0.4 on 2024-07-05 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChessPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('title', models.CharField(default='no title', max_length=100)),
                ('rating', models.PositiveIntegerField(default=1500)),
                ('games_played', models.PositiveIntegerField(default=0)),
                ('games_won', models.PositiveIntegerField(default=0)),
                ('games_lost', models.PositiveIntegerField(default=0)),
                ('games_drawn', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Dungeon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=10)),
                ('location', models.CharField(max_length=100)),
                ('boss_name', models.CharField(max_length=100)),
                ('recommended_level', models.PositiveIntegerField()),
                ('boss_health', models.PositiveIntegerField()),
                ('reward', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('meal_type', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], max_length=10)),
                ('preparation_time', models.CharField(max_length=30)),
                ('difficulty', models.PositiveIntegerField()),
                ('calories', models.PositiveIntegerField()),
                ('chef', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('workout_type', models.CharField(choices=[('Cardio', 'Cardio'), ('Strength', 'Strength'), ('Yoga', 'Yoga'), ('CrossFit', 'CrossFit'), ('Calisthenics', 'Calisthenics')], max_length=20)),
                ('duration', models.CharField(max_length=30)),
                ('difficulty', models.CharField(max_length=50)),
                ('calories_burned', models.PositiveIntegerField()),
                ('instructor', models.CharField(max_length=100)),
            ],
        ),
    ]
