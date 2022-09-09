from django.db import models

# Create your models here.


class Search (models.Model):

    GENDER_CHOISES = [
        ('m', 'Парень'),
        ('f', 'Девушка')
    ]

    nickname = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOISES, blank=True, null=True)
    similar = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname



