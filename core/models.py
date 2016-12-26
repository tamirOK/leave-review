# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import User
from datetime import datetime

from django.db import models
# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Faculties"

    def __unicode__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculty)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    year = models.DateField()
    group = models.CharField(max_length=15)
    specialization = models.ForeignKey(Specialization)
    photo = models.ImageField(blank=True, null=True, upload_to='students')

    def get_faculty(self):
        return self.specialization.faculty

    def __unicode__(self):
        return self.name + " " + self.surname


class Review(models.Model):
    review = models.TextField()
    date = models.DateTimeField('date created', default=datetime.now)
    about = models.ForeignKey(Student)
    author = models.ForeignKey(User)
