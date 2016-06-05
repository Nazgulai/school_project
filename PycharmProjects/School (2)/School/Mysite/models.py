 #-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import timedelta, datetime
from django.template.defaultfilters import date
from django.utils.html import format_html
from django.utils.text import slugify
from django.contrib import admin
# Create your models here.
class Article(models.Model):
    class Meta:
        verbose_name_plural= 'Жаңылыктар'
        verbose_name= 'Жаңылык'

    title = models.CharField('Аталышы', max_length=200,blank=True)
    image = models.ImageField('Сүрөт',upload_to='Новости', null=True, blank=False)
    text = models.TextField('Текст')
    date = models.DateTimeField('Датасы')
    likes = models.IntegerField('Жактырылды', default=0)

    def __unicode__(self):
        return (self.title)

class Comments(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарийлер'
    name = models.CharField('Аты',max_length=50,null=False)
    date = models.DateField(auto_now_add=True)
    text = models.TextField('Текст')
    comments_article = models.ForeignKey(Article, verbose_name='Жаңылыктын Комментарийи')

    def __unicode__(self):
        return (self.name)

# class Slider(models.Model):
#     class Meta:
#         permissions=(("can_deliver_pizzas", "Can deliver pizzas"),)
#         verbose_name='Фотография'
#         verbose_name_plural='Фотографии'
#     title=models.CharField('Название', max_length=100)
#     image=models.ImageField('Фотография', null=True, blank=False)
#     date=models.DateField('Дата', auto_now_add=True)
#     def __unicode__(self):
#         return (self.title)

# class Person(models.Model):
#     name = models.CharField(max_length=50)
#     birthday = models.DateField()
#     last_name = models.CharField(max_length=100)
#
#
#     def baby_boomer_status(self):
#         "Returns the person's baby-boomer status."
#         import datetime
#         if self.birthday < datetime.date(1945, 8, 1):
#             return "Pre-boomer"
#         elif self.birthday < datetime.date(1965, 1, 1):
#             return "Baby boomer"
#         else:
#             return "Post-boomer"
#     # def __unicode__(self):
#     #     return (self.name)
#     # def get_ful_name(self):
#     #     return '%s %s' %(self.name,self.last_name)
#     # ful_name = property(get_ful_name)
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    # def baby_boomer_status(self):
    #     "Returns the person's baby-boomer status."
    #     import datetime
    #     if self.birthday < datetime.date(1945, 8, 1):
    #         return "Pre-boomer"
    #     elif self.birthday < datetime.date(1965, 1, 1):
    #         return "Baby boomer"
    #     else:
    #         return "Post-boomer"
    def __unicode__(self):
        return (self.last_name)
# class MyPerson(Person):
#              class Meta:
#                 proxy = True
class OrderedPerson(Person):
            class Meta:
                ordering = ["last_name"]
                proxy = True

class Images(models.Model):
    image=models.ImageField(upload_to='media_ms')
    date=models.DateTimeField(auto_now_add=True)

class Album(models.Model):
    name=models.CharField(max_length=200)
    images=models.ManyToManyField(Images)


#     def save(self,*args,**kwargs):
#         if self.first_name=='Naz'and self.last_name=='Shergazieva':
#             return
        # else:
        #     super(Person,self).save(*args,**kwargs)
    # def get_ful_name(self):
    #     return '%s %s' %(self.first_name,self.last_name)
    # ful_name = property(get_ful_name)

# class Image(models.Model):
#     image = models.ImageField(upload_to="media_ms")
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey("content_type", "object_id")
# class Slider(models.Model):
#     name = models.CharField(max_length=100)

#     @classmethod
#     def create(cls,name):
#         product=cls(name=name)
#         return product
# product = Product.create("NNNNNN")

class Nazgul(models.Model):
    name=models.CharField(max_length=11)

class Files(models.Model):
     file = models.FileField(upload_to='files')
     title = models.CharField(max_length=100)
     date = models.DateTimeField()

     def __unicode__(self):
         return (self.title)

class Property(models.Model):
    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомдор'
    title=models.CharField('Аты',max_length=200)

    def __unicode__(self):
        return (self.title)

    def get_image(self):
        return PropertyImage.objects.filter(property_id=self.id)[0].image



class PropertyImage(models.Model):
    property=models.ForeignKey(Property, verbose_name='Cүрөт')
    image=models.ImageField(upload_to='Album', verbose_name='Сүрөт')