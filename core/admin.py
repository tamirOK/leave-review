# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from core.models import Student, Specialization, Faculty
# Register your models here.

admin.site.register(Student)
admin.site.register(Specialization)
admin.site.register(Faculty)
