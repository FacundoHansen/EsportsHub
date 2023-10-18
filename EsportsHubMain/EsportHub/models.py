from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed_teams = models.ManyToManyField('Team', blank=True)
    email = models.EmailField(default='example@example.com')  # Valor predeterminado
    def __str__(self):
        return self.user.username

    def is_following_team(self, team):
        return team in self.followed_teams.all()

class Videogame(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False)
    def __str__(self):
        return self.name

class Team(models.Model):
    acronym = models.CharField(max_length=10, null=True, blank=True)
    current_videogame = models.ForeignKey(Videogame, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField()
    slug = models.SlugField(unique=False)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Player(models.Model):
    age = models.PositiveIntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True)
    modified_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=2)
    role = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=False)
    team = models.ForeignKey(Team, related_name="players", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
