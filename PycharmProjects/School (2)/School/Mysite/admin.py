from datetime import date
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from Mysite import models
from Mysite.models import Article,Comments,Person,OrderedPerson, Nazgul, Images, Album, Files,PropertyImage,Property


class ArticleInline(admin.StackedInline):
    # fk_name = ['comments_article_id']
    model = Comments
    fk_name = "comments_article"
    extra = 5
    # raw_id_fields = ['comments_article']
    # verbose_name = ['comment']
    # min_num = 1
    # def get_extra(self, request, obj=None, ** kwargs):
    #     extra = 5
    #     if obj:
    #         return extra - obj.comments_set.count()
    #     return extra
class CommentsAdmin(admin.ModelAdmin):
    # radio_fields = {'comments_article':admin.HORIZONTAL}
    # raw_id_fields = ['comments_article']
    readonly_fields = ['comments_article']
class ArticleAdmin(admin.ModelAdmin):
    fields = ('title','image','text','date')
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct= super(ArticleAdmin,self).get_search_results(request,queryset,search_term)
        try:
            search_term_as_int=int(search_term)
        except ValueError:
            pass
        else:
            queryset |=self.model.objects.filter(id=search_term_as_int)
        return queryset,use_distinct

    # empty_value_display = '-e101mpty-'
    list_display = ('id','title','date','likes')
    list_display_links = ('id','title')
    # ordering = ['-date']
    # list_editable = ['title']
    # save_as = True
    # save_on_top = /True
    # search_fields = ['title']
    # view_on_site = False
    # show_full_result_count = True
    # prepopulated_fields = {"text": ('text',)}
    # raw_id_fields = ['title']
    # list_filter = ['date' ]
    # list_select_related = ['']
    inlines = [ArticleInline]
    # radio_fields = {'comments_article'}
    # # date_hierarchy = 'date'
    # # readonly_fields = ['title']
    # def lower_case_name(self,obj):
    #     return ("%s " %(obj.title,)).lower()
    # lower_case_name.short_description='Name'
    # lower_case_name.empty_value_display='????'
    #         #   list_display=(lower_case_name)
    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

# class SliderAdmin(admin.ModelAdmin):
#     fields = ['title','image']

class DecadeBornListFilter(admin.SimpleListFilter):
# Human-readable title which will be displayed in the
# right admin sidebar just above the filter options.
    title = _('decade born')
# Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'
    def lookups(self, request, model_admin):
        return (
                    ('80s', _('in the eighties')),
                    ('90s', _('in the nineties')),
                )
    def queryset(self, request, queryset):
        if self.value() == '80s':
            return queryset.filter(birthday__gte=date(1980, 1, 1),
            birthday__lte=date(1989, 12, 31))
        if self.value() == '90s':
            return queryset.filter(birthday__gte=date(1990, 1, 1),
            birthday__lte=date(1999, 12, 31))
class PersonAdmin(admin.ModelAdmin):
    list_display = ['get_absolute_url']
    def get_absolute_url(self,obj):
        return obj.last_name
# class OrderedPerson(admin.ModelAdmin):
    # list_filter = (DecadeBornListFilter,)
# class PersonAdmin(admin.ModelAdmin):
#     def decade_born_in(self):
#         return self.birthday.strftime('%Y')[:3] == '195'
#     decade_born_in.boolean = True
#     decade_born_in.short_description = 'Birth decade'
#     # birth_date = property(decade_born_in)
#     # decade_born_in.admin_order_field='-decade__born_in'
#     list_display = ('name', decade_born_in)
#     # ordering = [decade_born_in]


# class PersonAdmin(admin.ModelAdmin):
#     def colored_name(self):
#         return format_html('<span style="color: #{};">{} {}</span>',
#                 self.color_code,
#                 self.first_name,
#                 self.last_name)
# list_display = ( 'colored_name')
#
# class ImageInline(GenericTabularInline):
#     model = Image
#     extra = 2
# class SliderAdmin(admin.ModelAdmin):
#     inlines = [
#     ImageInline,
#     ]
#     list_display = ['name']
# admin.site.register(Slider, SliderAdmin)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ['date']
#
# class AlbumAdmin(admin.ModelAdmin):
#     list_display = ['name']
class PropertyImageInline(admin.TabularInline):
    model=PropertyImage
    extra = 3
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]


admin.site.register(Article,ArticleAdmin)
admin.site.register(OrderedPerson)
admin.site.register(Person,PersonAdmin)
admin.site.register(Comments,CommentsAdmin)
# admin.site.register(Album)
# admin.site.register(Images)
admin.site.register(Nazgul)
admin.site.register(Album)
admin.site.register(Images)
admin.site.register(Files)
admin.site.register(Property,PropertyAdmin)


