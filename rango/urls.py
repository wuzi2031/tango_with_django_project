#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/26 14:55
# @Author  : Aries
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from rango import views
urlpatterns=[url(r'^$',views.index,name='index'),
             url(r'^about/',views.about,name='about'),]