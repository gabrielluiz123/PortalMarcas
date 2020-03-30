from django.contrib import admin
from .models import Cms, Cms_Slider
from django_summernote.admin import SummernoteInlineModelAdmin


class CmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca')
    list_display_links = ('id', 'marca')

class Cms_SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao')
    list_display_links = ('id', 'descricao')


admin.site.register(Cms_Slider, Cms_SliderAdmin)
admin.site.register(Cms, CmsAdmin)

