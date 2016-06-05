from audioop import reverse
from django.views.decorators.csrf import  csrf_protect
from Journal.forms import GroupSelectForm, SubjectSelectForm, PointForm
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.contrib import auth
from django.views.generic import TemplateView
from models import *


class TimeTableView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        form = GroupSelectForm()
        context = {}
        if request.method == "POST":
            form = GroupSelectForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data['group']
                subject = form.cleaned_data['subject']
                context['group'] = group
                lessons_by_days = self.get_lessons(group)
                context['lessons_by_days'] = lessons_by_days

        context['form'] = form
        return render(request, "Journal/timetable.html", context)

    def get_lessons(self, group):
        lessons = LessonsDay.objects.filter(subject__group=group)
        days = Day.objects.all().order_by("order")
        lessons_by_days = {}
        for day in days:
            lessons_by_days[day] = []

        for lesson in lessons:
            for day in lesson.days.all():
                lessons_by_days[day].append(lesson)

        return lessons_by_days
# #

# class HomePageView(TemplateView):
#     template_name = 'Journal/home.html'
#     def get_context_data(self, **kwargs):
#         context=super(HomePageView,self).get_context_data(**kwargs)
#         context['latestlessons']= LessonsDay.objects.all()[:5]
#         return context
#
def get_students(group):
    students_by_group = Student.objects.filter(current_group=group)
    return students_by_group




class TeacherPageView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        form = GroupSelectForm()
        context = {}
        period, months = self.get_period()
        context['period'] = period
        context['months'] = months
        if request.method == 'POST':
            form = GroupSelectForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data['group']
                subject = form.cleaned_data['subject']
                context['group'] = group
                students = self.get_students(group)
                context['students'] = students
                if 'set_points' in request.POST:
                    self.set_points(request, students, subject, period)
                context['points'] = self.get_points(students, subject, period)
        context['form'] = form

        return render(request, 'Journal/home.html', context)

    def set_points(self, request, students, subject, period):
        for student in students:
            points_array = request.POST.getlist(u'student_%d' % student.id)
            for i in range(0, len(period)-1):
                date = period[i]
                point = points_array[i]
                if len(point.strip()) > 0:
                    if Point.objects.filter(student=student, date=date, subject=subject).count() == 0:
                        point_object = Point(student=student, point=point, date=date, subject=subject)
                        point_object.save()

    def get_points(self, students, subject, period):
        points = {}
        for student in students:
            points[student.id] = {}
            for date in period:
                try:
                    point = Point.objects.get(student=student, date=date, subject=subject)
                    points[student.id][date] = point.point
                except Point.DoesNotExist:
                    points[student.id][date] = None
        return points

    def get_students(self, group):
        students_by_group = Student.objects.filter(current_group=group)
        return students_by_group

    def get_period(self):
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt','Nov', 'Dec']
        months = []
        start = datetime(2016, 04, 01)
        end = datetime(2016, 05, 30)
        delta = (end - start).days
        period = []
        month = start.month
        days = 0
        for i in range(delta):
            date = start + timedelta(i)
            if month == date.month:
                days += 1
            else:
                months.append((month_names[month-1],days))
                month = date.month
                days = 1
            period.append(date)
        months.append((month_names[month-1], days))
        return period, months


class SetPointsView(TemplateView):
    template_name = "Journal/home.html"





def teacher_login_portal(request):
    c={}
    c.update(csrf(request))
    return render_to_response('Journal/teacher_login_portal.html', c)

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return loggedin(request)
    else:
        c={'error':'error'}
        c.update(csrf(request))
        return render_to_response('Journal/teacher_login_portal.html', c)


def loggedin(request):
    return render_to_response('Journal/loggedin.html',
                              {'full_name': request.user.get_full_name,
                               }
                              )
def invalid(request):
    return render_to_response('Journal/invalid.html')

def logout(request):
    auth.logout(request)
    return redirect(reverse("teacher_login_portal"))