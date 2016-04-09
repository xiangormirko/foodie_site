from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import validators


# Create your models here.


class List(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, validators=[validators.MaxLengthValidator(100)])
    description = models.TextField()
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User)
    tags = TaggableManager(blank=True)
    thumb = models.ImageField(upload_to='rest_pics', blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lists:detail', kwargs={
            'pk': self.id,
        })


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    website = models.URLField(blank=True)
    tags = TaggableManager(blank=True)
    thumb = models.ImageField(upload_to='rest_pics', blank=True)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=180)
    restaurants = models.ManyToManyField(Restaurant)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    following = models.ManyToManyField(List)

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    posted_time = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User)
    content = models.TextField(blank=True)
    username = models.CharField(max_length=180, blank=True)
    avatar = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ('posted_time',)
