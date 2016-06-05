# coding=utf-8
from Journal.models import Group, Subject, Point
from django import forms
from django.forms import Form, ModelForm


class GroupSelectForm(Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label=u"Класс")
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label=u"Предмет")


class SubjectSelectForm(Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(),label=u"Предмет")


class PointForm(ModelForm):
    class Meta:
        model=Point
        fields= ['point']