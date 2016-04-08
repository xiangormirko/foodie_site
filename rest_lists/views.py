from django.http import HttpResponse
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, Http404, render_to_response
from django.db.models import Q, Count, Sum
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout

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
        print('crap!')
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
            list.save()
            return HttpResponseRedirect(list.get_absolute_url())

    return render(request, 'rest_lists/list_form.html', {'form': form})


@login_required
def create_rest(request, list_pk ):
    form = forms.RestForm()
    list = get_object_or_404(models.List, pk = list_pk)

    return render(request, 'rest_lists/rest_form.html', {'form': form, 'list': list})


