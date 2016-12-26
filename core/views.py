# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Student, Faculty, Specialization, Review


def index(request):
    if request.method == 'GET':
        faculties = Faculty.objects.distinct()
        message = request.session.get('message', "")
        students = Student.objects.filter(specialization__faculty__name='Инженерный')
        paginator = Paginator(students, 4)
        students = paginator.page(1)
        context = {'faculties': faculties, 'message': message,
                   'students': students}
        return render(request, 'core/new_index.html', context)


@csrf_protect
def get_specialization(request):
    if request.method == 'GET':
        if request.GET.get('faculty', None) is not None:
            faculty = request.GET['faculty']
            specializations = Specialization.objects.filter(faculty__name=faculty)
            return render(request, 'core/specializations.html',
                          {'specializations': specializations})


def get_students_by_faculty(request):
    if request.method == 'GET':
        faculty = request.GET['faculty']
        students = Student.objects.filter(specialization__faculty__name=faculty)
        paginator = Paginator(students, 4)
        page = int(request.GET.get('page', 1))
        try:
            students = paginator.page(page)
        except PageNotAnInteger or EmptyPage:
            students = paginator.page(1)

        context = {'students': students}
        return render(request, "core/new_subtemplate.html", context)


def get_students(request):
    if request.method == 'GET':
        page = request.GET['page']
        specialization = request.GET.get('specialization', None)
        faculty = request.GET.get('faculty', None)
        context = {'specialization': True}
        print faculty, specialization
        if specialization is not None:
            students = Student.objects.filter(specialization__name=specialization)
        else:
            del context['specialization']
            students = Student.objects.filter(specialization__faculty__name=faculty)
        paginator = Paginator(students, 4)
        try:
            students = paginator.page(int(page))
            print "ok"
        except PageNotAnInteger or EmptyPage:
            students = paginator.page(1)
        context['students'] = students
        return render(request, 'core/new_subtemplate.html', context)


def student_info(request, name, surname):
    if request.method == 'GET':
        student = get_object_or_404(Student, name=name, surname=surname)
        reviews = Review.objects.filter(about__name=name, about__surname=surname).order_by('-date')
        return render(request, 'core/all_reviews.html',
                      {'reviews': reviews, 'name': name, 'surname': surname,
                       'year': student.year.year,
                       'specialization': student.specialization.name,
                       'photo_url': student.photo,
                       })


@login_required
def add_rev(request):
    if request.method == 'GET':
        author = request.user
        about = Student.objects.get(name=request.GET['name'], surname=request.GET['surname'])
        date = datetime.now()
        review = Review(date=date, about=about, author=author, review=request.GET['content'])
        review.save()
        reviews = Review.objects.filter(about__name=about.name, about__surname=about.surname).order_by('-date')
        return render(request, 'core/updated_reviews.html',
                      {'reviews': reviews, })


def student_search(request):
    name = request.GET.get('name', None)
    surname = request.GET.get('surname', None)
    if name == "-1":
        a = Student.objects.filter(specialization__faculty__name='Инженерный')
        students = Paginator(a, 4).page(1)
        return render(request, 'core/new_subtemplate.html',
                      {'students': students})

    if name is None:
        name = ""
    if surname is None:
        surname = ""

    students_list1 = Student.objects.filter(Q(name__startswith=name, surname__startswith=surname)
                                            | Q(name__startswith=surname, surname__startswith=name))
    students = students_list1
    paginator = Paginator(students, 4)
    students = paginator.page(1)
    context = {'students': students}
    return render(request, 'core/new_subtemplate.html', context)



