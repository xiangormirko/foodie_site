from django import forms
from django.core import validators
from django.contrib.auth.models import User
from .models import UserProfile

from . import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    verify_password = forms.CharField(label="please verity your password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        verity = cleaned_data.get('verify_password')

        if password != verity:
            raise forms.ValidationError(
                "Passwords are not matching"
            )


class EditUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(label="new password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'old_password', 'new_password')

        # def clean(self):
        #     cleaned_data = super().clean()
        #     password = cleaned_data.get('password')
        #     verity = cleaned_data.get('verify_password')
        #
        #     if password != verity:
        #         raise forms.ValidationError(
        #             "Passwords are not matching"
        #         )


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
            'website',
            'tags',
            'thumb',
        ]


class ChatForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = models.Chat
        fields = [
            'content',
        ]
