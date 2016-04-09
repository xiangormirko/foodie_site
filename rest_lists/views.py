from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, Http404, render_to_response
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib import messages
import json

from . import forms
from . import models

# Create your views here.

from .models import List, Restaurant


def list_all(request):
    lists = List.objects.all()
    list_id = None

    if request.method == 'GET':
        list_id = request.GET.get('list_id', False)
    if list_id:
        list = List.objects.get(id=list_id)
        print(list)

        likes = list.likes + 1
        list.likes = likes
        list.save()
        return HttpResponse(likes)


    return render(request, 'rest_lists/list_all.html', {'lists': lists})


def register(request):
    """
    handling register functions
    :param request:
    :return: renders the page again and changes depending if the user completed registration
    """
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rest_lists/register.html', {
        'user_form': user_form, 'profile_form': profile_form, 'registered': registered
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/lists/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # bad login
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rest_lists/login.html', {})

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


def list_detail(request, pk):
    try:
        list = models.List.objects.prefetch_related(
            'restaurant_set'
        ).get(pk=pk)
    except models.List.DoesNotExist:
        raise Http404
    else:
        restaurants = list.restaurant_set.all()

    if request.method == 'POST':
        rest = models.Restaurant.objects.get(id = request.POST.get('rest_pk'))
        rest.delete()
        print('rest deleted')
        return HttpResponse(request.POST.get('rest_pk'))


    return render(request, 'rest_lists/list_detail.html', {
        'list': list,
        'restaurants' : restaurants
    })


@login_required
def create_list(request):
    form = forms.ListForm()
    if request.method == 'POST':
        form = forms.ListForm(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            list.owner = request.user
            if 'thumb' in request.FILES:
                list.thumb = request.FILES['thumb']
            list.save()
            form.save_m2m()
            return HttpResponseRedirect(list.get_absolute_url())

    return render(request, 'rest_lists/list_form.html', {'form': form, 'user': request.user})


@login_required
def create_rest(request, list_pk ):
    form = forms.RestForm()
    list = get_object_or_404(models.List, pk = list_pk)

    if request.method == 'POST':
        form = forms.RestForm(request.POST)
        if form.is_valid():
            rest = form.save(commit=False)
            rest.list = list
            if 'thumb' in request.FILES:
                rest.thumb = request.FILES['thumb']
            rest.save()
            form.save_m2m()
            return HttpResponseRedirect(list.get_absolute_url())

    return render(request, 'rest_lists/rest_form.html', {'form': form, 'list': list})

@login_required
def chat_room(request):
    form = forms.ChatForm(request.POST)
    if request.method == 'POST':
        form = forms.ChatForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.poster = request.user
            post.username = request.user.username
            post.avatar = request.user.userprofile.picture
            post.save()
            posts = models.Chat.objects.all()
            return render(request, 'rest_lists/chatroom.html', {'posts': posts, 'form': form})
            return HttpResponse(serializers.serialize('json', models.Chat.objects.all()))

    if request.method == 'GET':
        if request.is_ajax():
            posts = serializers.serialize('json', models.Chat.objects.all())
            return HttpResponse(posts)

    posts = models.Chat.objects.all()

    return render(request, 'rest_lists/chatroom.html', {'posts': posts, 'form': form})

@login_required
def profile_page(request):
    user = request.user
    user_profile = request.user.userprofile
    form = forms.EditUserForm(instance=user)
    profile_form = forms.UserProfileForm(instance=user.userprofile)
    if request.method == 'POST':
        form = forms.EditUserForm(request.POST, instance=user)
        profile_form = forms.UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid and profile_form.is_valid():
            if request.POST.get('old_password'):
                if user.check_password(request.POST.get('old_password')):
                    user = form.save()
                    user.set_password(request.POST.get('new_password'))
                    user.save()
                else:
                    messages.error(request, "passwod didn't match the old one")
            else:
                user = form.save()
                user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Profile Edited!")
            return HttpResponseRedirect('/lists/profile')
    lists = models.List.objects.filter(owner=user)
    print(lists)
    return render(request, 'rest_lists/user_page.html', {'form': form, 'profile_form': profile_form, 'lists': lists})

@login_required
def list_edit(request, list_pk):
    edit = True
    list = get_object_or_404(models.List, pk=list_pk)
    form = forms.ListForm(instance=list)

    if request.method == 'POST':
        form = forms.ListForm(request.POST, instance=list)
        if form.is_valid():
            if request.POST.get('delete_btn'):
                print("delete")
                form.save()
                list = form.save(commit=False)
                list.delete()
                messages.success(request, "Deleted {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect('/lists/')
            else:
                form.save()
                messages.success(request, "Updated {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect('/lists/')

    return render(request, 'rest_lists/list_form.html', {'form': form, 'user': request.user, 'edit':edit})

def search_by_tags(request):
    lists = None
    rests  = None

    if request.method =='POST':
        keyword = request.POST.get('keyword')
        lists = models.List.objects.filter(tags__name__in=[keyword])
        rests = models.Restaurant.objects.filter(tags__name__in=[keyword])

        return render(request, 'rest_lists/search.html', {'lists': lists, 'rests': rests})
    return render(request, 'rest_lists/search.html', {'lists': lists, 'rests': rests})
