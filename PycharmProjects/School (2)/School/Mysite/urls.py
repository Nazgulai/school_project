from django.conf.urls import url

import Mysite,Journal
from . import views

# app_name = 'Journal'
urlpatterns = [
url(r'^$', Mysite.views.base_home, name='base_home'),
# url(r'^users/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
# url(r'^parent_login_portal/$', Mysite.views.parent_login_portal, name='parent_login_portal'),
# url(r'^teacher_login_portal/$', Mysite.views.teacher_login_portal, name='teacher_login_portal'),
# url(r'^auth/$', Mysite.views.auth_view, name='auth_view'),
# url(r'^loggedin/$', Mysite.views.loggedin, name='loggedin'),
# url(r'^logout/$', Mysite.views.logout, name='logout'),
# url(r'^invalid/$', Mysite.views.invalid, name='invalid'),
# url(r'^student_login_portal/$', Mysite.views.student_login_portal, name='student_login_portal'),
url(r'^gallery/$', Mysite.views.gallery, name='gallery'),
url(r'^images/get/(?P<property_id>\d+)/$', Mysite.views.images, name='images'),
url(r'^home_article/get/(?P<article_id>\d+)/$', Mysite.views.home_article, name='home_article'),
url(r'^home_article/addcomment/(?P<article_id>\d+)/$', Mysite.views.addcomment, name='addcomment'),
url(r'^base_home/addlike/(?P<article_id>\d+)/$',Mysite.views.addlike,name='addlike' ),

]
