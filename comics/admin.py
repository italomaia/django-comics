#-*- coding: utf-8 -*-

from django.contrib import admin
from models import WebComic, Strip, BlogPage

#class WebComicAdmin(admin.ModelAdmin):
    #form = WebComicForm

#class ComicStripAdmin(admin.ModelAdmin):
    #form = ComicStripForm
admin.site.register(WebComic)
admin.site.register(Strip)
admin.site.register(BlogPage)

#comics_admin.register(WebComic, WebComicAdmin)
#comics_admin.register(Strip, ComicStripAdmin)