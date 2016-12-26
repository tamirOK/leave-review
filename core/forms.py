# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('review', )
        widgets = {
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
