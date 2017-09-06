# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url']


# Register your models here.
admin.site.register(Category, admin_class=CategoryAdmin)
admin.site.register(Page, admin_class=PageAdmin)
