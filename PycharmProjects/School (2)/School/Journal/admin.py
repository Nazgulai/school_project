# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *


# Register your models here.


class QuarterInline(admin.StackedInline):
    model = Quarter


class SchoolYearAdmin(admin.ModelAdmin):
    class Meta:
        model = SchoolYear

    list_display = 'start finish'.split()
    inlines = [QuarterInline]


class SubjectInline(admin.StackedInline):
    model = Subject


class StudentInline(admin.StackedInline):
    model = Student


class GroupAdmin(admin.ModelAdmin):
    class Meta:
        model = Group

    list_display = 'grade nominal school_year'.split()
    inlines = [StudentInline, SubjectInline]


class StudentAdmin(admin.ModelAdmin):
    class Meta:
        model = Student

    list_display = 'first_name last_name'


# class SubjectAdmin(admin.ModelAdmin):
#    class Meta:
#        model = Subject
#    list_display = '__unicode__ school_year teacher group'.split()


# class SubjectDayInline(admin.StackedInline):
#     model = SubjectDay


# class LessonsDayAdmin(admin.ModelAdmin):
#     class Meta:
#         model = LessonsDay

    # inlines = [SubjectDayInline]


admin.site.register(Student)
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(Group, GroupAdmin)
# admin.site.register(LessonsDay, LessonsDayAdmin)
admin.site.register(Subject)
admin.site.register(Point)
admin.site.register(Day)
# admin.site.register(Parent)
admin.site.register(Teacher)