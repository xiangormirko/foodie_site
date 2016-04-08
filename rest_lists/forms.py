from django import forms
from django.core import validators
from django.contrib.auth.models import User
from .models import UserProfile

from . import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class ListForm(forms.ModelForm):
    class Meta:
        model = models.List
        fields = [
            'title',
            'description',
            'tags',
            'thumb',
            'public',

        ]

class RestForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            'name',
            'address',
            'url',
            'tags',
            'thumb',
        ]