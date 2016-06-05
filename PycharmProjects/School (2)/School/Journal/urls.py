from Journal.views import TimeTableView
from Journal.views import TeacherPageView
from django.conf.urls import url
from . import views
import Mysite,Journal
urlpatterns = [
    # url(r'^$', TimeTableView.as_view(), name='timetable'),
    # url(r'^$', TeacherPageView.as_view(), name='home'),
    # url(r'^home/addpoint/$',Journal.views.SetPointsView.as_view(), name='addpoint')
    url(r'^$', Journal.views.teacher_login_portal, name='teacher_login_portal'),
    url(r'^auth/$', Journal.views.auth_view, name='auth_view'),
    url(r'^loggedin/$', Journal.views.loggedin, name='loggedin'),
    url(r'^$', Journal.views.logout, name='logout'),
    # url(r'^invalid/$', Journal.views.invalid, name='invalid'),
]
