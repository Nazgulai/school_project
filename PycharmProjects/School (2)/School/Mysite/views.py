from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from Mysite.forms import CommentsForm
from Mysite.models import Article,Comments, Files, Property,PropertyImage


# def base_home(request):
#     article=Article.objects.all()[:3]
#     return render(request,'Mysite/base_home.html',{'article':article} )

# def home_article(request,article_id):
#
#     article=Article.objects.get(id=article_id)
#     comment=Comments.objects.filter(comments_article_id=article_id)
#     return render(request,'Mysite/home_article.html',{'article':article,'comment':comment})
def home_article(request,article_id):
    comment_form=CommentsForm
    args={}
    args.update(csrf(request))
    args['article']=Article.objects.get(id=article_id)
    args['comment']=Comments.objects.filter(comments_article_id=article_id)
    args['form']=comment_form
    return render_to_response('Mysite/home_article.html',args)

def addcomment(request,article_id):
    if request.POST:
        form=CommentsForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.comments_article=Article.objects.get(id=article_id)
            comment.save()
            return redirect('home_article', article_id)

def addlike(request, article_id):
    try:
        article=Article.objects.get(id=article_id)
        article.likes+=1
        article.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect('base_home')

def base_home(request):
    # property = Property.objects.get(pk=2)
    # image_list = property.images.get(pk=9)
    article = Article.objects.order_by('date')
    paginator = Paginator(article, 3) # Show 25 contacts per page
    page = request.GET.get('page')

    try:
        article = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        article = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        article = paginator.page(paginator.num_pages)
    return render(request, 'Mysite/base_home.html', {'article': article  })

def gallery(request):
    album=Property.objects.all()
    return render( request,'Mysite/gallery.html', {'album':album })

def images(request,property_id):
    args = {}
    args['alb']= Property.objects.get(id=property_id)
    args ['images']= PropertyImage.objects.filter(property_id=property_id)
    return render_to_response('Mysite/images.html',args)

# def parent_login_portal(request):
#     return render(request, 'Mysite/parent_login_portal.html')
# @csrf_protect
# def teacher_login_portal(request):
#     c={}
#     c.update(csrf(request))
#     return render_to_response('Mysite/teacher_login_portal.html', c)
#
# def auth_view(request):
#     username = request.POST.get('username','')
#     password = request.POST.get('password','')
#     user = auth.authenticate(username=username,password=password)
#
#     if user is not None:
#         auth.login(request,user)
#         return loggedin(request)
#     else:
#         c={'error':'error'}
#         c.update(csrf(request))
#         return render_to_response('Mysite/teacher_login_portal.html', c)
#
#
# def loggedin(request):
#     return render_to_response('Mysite/loggedin.html',
#                               {'full_name': request.user.get_full_name,
#                                }
#                               )
# def invalid(request):
#     return render_to_response('Mysite/invalid.html')
#
# def logout(request):
#     auth.logout(request)
#     return redirect(reverse("teacher_login_portal"))
# #
# def student_login_portal(request):
#     return render(request, 'Mysite/student_login_portal.html')

# def parent_login_portal(request):
#     return render(request, 'Mysite/parent_login_portal.html')
#
