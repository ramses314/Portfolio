from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.


class Post(models.Model):

    user = models.ForeignKey(User, related_name='post_created', on_delete=models.CASCADE)
    # title = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='media/posts/%Y/%m/%d', blank=True, null=True)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    users_like = models.ManyToManyField(User, related_name='posts_liked', blank=True)


    def __str__(self):
        return self.body


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.body[:50])
        super(Post, self).save(*args, **kwargs)
