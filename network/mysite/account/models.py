from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


# Create your models here.

from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image):
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=60)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, default='media/defaultr/zero_photo.jpg')
    status = models.TextField(default='Привет, я новый пользователь')
    tags = TaggableManager(blank=True)

    GENDER_CHOISES = [
        ('m', 'Парень'),
        ('f', 'Девушка')
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOISES, blank=True, null=True)

    def save(self, *args, **kwargs):
        # call the compress function
        new_image = compress(self.image)
        # set self.image to new_image
        self.image = new_image
        # save
        super().save(*args, **kwargs)



    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} foller to {}'.format(self.user_from, self.user_to)

User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers',
                                                      symmetrical=False))