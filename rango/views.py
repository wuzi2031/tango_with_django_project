# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage':"I am bold font from the context"}
    # return HttpResponse("Rango says hey there world!<br/><a href='/rango/about'>About</a>")
    return render(request,'rango/index.html',context_dict)
def about(request):
    context_dict = {'aboutmessage': "Here is the about page!"}
    return render(request,'rango/about.html',context_dict)