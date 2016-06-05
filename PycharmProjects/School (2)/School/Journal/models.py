# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.conf import settings
# from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta, datetime
from django.template.defaultfilters import date
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from School import settings


def image_upload_to(instance, filename):
    title = instance.id
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "images/%s/%s" % (slug, new_filename)


class SchoolYear(models.Model):
    class Meta:
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные года'

    start = models.DateField(_('Начало года'))
    finish = models.DateField(_('Конwf года'))

    def __unicode__(self):
        return '%s-%s'%(unicode(self.start.year), unicode(self.finish.year))


class Teacher(models.Model):
    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    image = models.ImageField(upload_to='media_ms', null=True, blank=True)
    teacher = models.ForeignKey(User)

    def __unicode__(self):
        return self.teacher.get_full_name()


class Group(models.Model):
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    GRADE_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
    )
    NOMINAL_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    grade = models.CharField(_('Класс'),max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    nominal = models.CharField(_('Аталма'),max_length=1, choices=NOMINAL_CHOICES, null=True, blank=True)
    school_year = models.ForeignKey(SchoolYear, verbose_name='Окуу жылы', blank=True)

    def __unicode__(self):
        return u"%s-%s" % (self.grade, self.nominal)


class Student(models.Model):
    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    first_name = models.CharField(_('Аты'),max_length=200)
    last_name = models.CharField(_('Фамилия'),max_length=200)
    middle_name = models.CharField(_('Отчество'),max_length=200)
    birthday = models.DateField(_('Туулган жылы'))
    address = models.CharField(_('Дарек'),max_length=200)
    phone = models.CharField(_('Телефон'),max_length=15, null=True)
    mother_phone = models.CharField(_('Апасынын номери'),max_length=200)
    father_phone = models.CharField(_('Атасынын номери'),max_length=200)
    starosta = models.BooleanField(_('Класс башчысы'),default=False)
    image = models.FileField(_('Сүрөт'),upload_to=image_upload_to, null=True, blank=True)
    current_group = models.ForeignKey(Group, related_name="CurrentGroup", null=True, verbose_name='Класс')

    def __unicode__(self):
        return '%s %s. %s.' % (self.last_name, self.first_name[0], self.middle_name[0])

    def get_points(self):
        return self.point_set.all()


class Quarter(models.Model):
    class Meta:
        verbose_name = 'Четверть'
        verbose_name_plural = 'Четверти'

    QUARTER_CHOICES = (('1', '1'),
                       ('2', '2'),
                       ('3', '3'),
                       ('4', '4'))
    quarter = models.CharField(_('Выбрать четверть'),max_length=1, choices=QUARTER_CHOICES)
    start = models.DateField(_('Начало четверти'))
    finish = models.DateField(_('Конец четверти'))
    school_year = models.ForeignKey(SchoolYear, blank=True)

    def __unicode__(self):
        return '%s  %s' % (self.quarter, self.school_year)


class Day(models.Model):
    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'

    name = models.CharField(max_length=30)
    order = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    NOMINAL_CHOICES = (
        ('Информатика', 'Информатика'),
        ('География', 'География'),
        ('История', 'История'),
        ('Математика', 'Математика'),
        ('Геометрия', 'Геометрия'),
        ('Русский язык', 'Русский язык'),
        ('История Кыргызстана', 'История Кыргызстана'),
        ('Кыргызский язык', 'Кыргызский язык'),
        ('Социология', 'Социология'),
        ('Химия', 'Химия'),
        ('Физика', 'Физика'),
        ('Биология', 'Биология'),

    )
    subject = models.CharField(_('Сабак '), max_length=200, choices=NOMINAL_CHOICES, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear, blank=True, verbose_name='Окуу жылы')
    teacher = models.ForeignKey(Teacher, verbose_name='Мугалим', blank=True)
    group = models.ForeignKey(Group, verbose_name='Класс', related_name="subjects")

    def __unicode__(self):
        return '%s %s %s-%s' % (self.teacher,self.subject, self.group.grade, self.group.nominal)


class LessonsDay(models.Model):
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
    # schoolyear = models.ForeignKey(SchoolYear,verbose_name='Окуу жылы')
    quarter = models.ForeignKey(Quarter, verbose_name='Чейрек')
    # group = models.ForeignKey(Group, verbose_name='класс')
    subject = models.ForeignKey(Subject, verbose_name='Сабак')
    days = models.ManyToManyField(Day,verbose_name='Күндөр')

    def __unicode__(self):
        return self.subject.__unicode__()

    def save(self, *args, **kwargs):
        super(LessonsDay, self).save(*args, **kwargs)
        days = ["Вс", 'Пн', "Вт", "Ср", "Чт", "Пт", "Сб"]
        SubjectDay.objects.filter(lessonsday_id=self.id).delete()
        for i in self.days.all():
            timestamp = self.quarter.start
            while timestamp != self.quarter.finish:
                a = (14 - int(timestamp.month)) // 12
                y = int(timestamp.year) - a
                m = int(timestamp.month) + 12 * a - 2
                weekday = (7000 + (int(timestamp.day) + y + y // 4 - y // 100 + y // 400 + (31 * m) / 12)) % 7
                if days[weekday] == i.name:
                    subjecttimestamp = SubjectDay.objects.create(day=timestamp, lessonsday_id=self.id)
                    subjecttimestamp.save()
                    Point.objects.filter(subjectday_id=subjecttimestamp.id).delete()
                    for j in Student.objects.filter(current_group=self.subject.group):
                        point = Point.objects.create(subjectday_id=subjecttimestamp.id,
                                                     student=j)
                        point.save()
                timestamp = timestamp + timedelta(days=1)
        super(LessonsDay, self).save(*args, **kwargs)


class SubjectDay(models.Model):
    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'

    day = models.DateField(_('Күн'),null=True, blank=True)
    lessonsday = models.ForeignKey(LessonsDay)

    def __unicode__(self):
        return '%s/%s/%s' % (self.day.day, self.day.month, self.day.year)

    def get_date(self):
        now = datetime.now()
        if date(now, 'Y/m/d') == date(self.day, 'Y/m/d'):
            return 'Бүгүн'
        elif date(now - timedelta(days=1), 'Y/m/d') == date(self.day, 'Y/m/d'):
            return 'Кечээ'
        else:
            return date(self.day, 'm/d/y')


class Point(models.Model):
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    # subjectday = models.ForeignKey(SubjectDay,verbose_name='Сабак')
    student = models.ForeignKey(Student, verbose_name='Окуучу')
    point = models.CharField(_('Баа'),default='#', max_length=4)
    date = models.DateField()
    subject = models.ForeignKey(Subject, verbose_name='Сабак', null=True)

    def __unicode__(self):
        return self.point


class Parent(models.Model):
    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'

    student = models.ManyToManyField(Student)
    parent = models.ForeignKey(User)

    def __unicode__(self):
        return self.parent.username

