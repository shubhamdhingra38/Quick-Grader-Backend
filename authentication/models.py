from django.db import models
from django.contrib.auth.models import User, Group

# User Profile Model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=500, blank=True, null=True)
    genderChoices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(choices=genderChoices, max_length=1)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.firstname + " " + self.lastname
