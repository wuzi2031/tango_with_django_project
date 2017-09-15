# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from rango.form import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if ((datetime.now() - last_visit_time).seconds > 0):
        visits += 1
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        response.set_cookie('last_visit', last_visit_cookie)
    response.set_cookie('visits', str(visits))


def index(request):
    # context_dict = {'boldmessage': "I am bold font from the context"}
    # return HttpResponse("Rango says hey there world!<br/><a href='/rango/about'>About</a>")
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    response = render(request, 'rango/index.html', context_dict)
    visitor_cookie_handler(request, response)
    return response


def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
    request.session.delete_test_cookie()
    context_dict = {'aboutmessage': "Here is the about page!"}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    try:
        # category = get_object_or_404(Category, slug=category_name_slug)
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category_name'] = category.name
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        return render(request, "rango/category.html", {'erro_message': "You didn't select a choice."})
    else:
        return render(request, "rango/category.html", context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    dict = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if (request.method == 'POST'):
        form = PageForm(request.POST)
        if (form.is_valid()):
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors

    else:
        form = PageForm()
    dict['form'] = form
    dict['category'] = cat
    return render(request, 'rango/add_page.html', dict)


def register(request):
    dict = {}
    registed = False
    if (request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if (user_form.is_valid() and profile_form.is_valid()):
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if ('picture' in request.FILES):
                profile.picture = request.FILES['picture']
            profile.save()
            registed = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    dict['user_form'] = user_form
    dict['profile_form'] = profile_form
    dict['registed'] = registed
    return render(request, 'rango/register.html', dict)


def user_login(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if (user):
            if (user.is_active):
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/user_login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    logout(request)
    return index(request)
