# coding=utf-8
from django.template import Library

register = Library()

def add_zero(number):
    if number<10:
        return u"0%d" % number
    else:
        return u"%d" % number


@register.filter
def kg_date(date):
    months = [u'январь', u'февраль', u'март', u'апрель', u'май', u'июнь', u'июль', u'август', u'сентябрь', u'октябрь', u'ноябрь',
              u'декабрь']
    return u"%d %s %d ж. %s:%s" % (date.day, months[date.month-1], date.year, add_zero(date.hour), add_zero(date.minute))


@register.assignment_tag
def get_students_point(points, student, date):
    return points[student.id][date]


@register.assignment_tag
def get_students_point(points, student, date):
    return points[student.id][date]


@register.assignment_tag
def get_students_point(points, student, date):
    return points[student.id][date]


@register.assignment_tag
def get_students_point(points, student, date):
    return points[student.id][date]
