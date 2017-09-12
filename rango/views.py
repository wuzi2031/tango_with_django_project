# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User
from rango.form import CategoryForm, PageForm, UserForm, UserProfileForm


def index(request):
    # context_dict = {'boldmessage': "I am bold font from the context"}
    # return HttpResponse("Rango says hey there world!<br/><a href='/rango/about'>About</a>")
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
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
