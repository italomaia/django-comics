#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list


from . import views
from .models import WebComic, Strip, BlogPage
from .forms import EditStripForm, EditWCForm

wc_list = {
    "queryset":WebComic.objects.all(),
    "template_name":"comics/index.html",
}

urlpatterns = patterns('',
    
    # showing all the webcomics
    (r'^$', object_list, wc_list, "comics-index"),
    
    (r'^edit/(?P<slug>[\d\w\-_]+)/$', views.edit, {}, "comics-edit-webcomic"),
    (r'^edit/(?P<slug>[\d\w\-_]+)/strip/(?P<pk>\d+)/$', views.edit, {}, "comics-edit-strip"),
    
    # shows webcomic (current strip)
    (r'^(?P<slug>[\d\w\-_]+)/$', views.show_webcomic, {}, "comics-webcomic"),
    
    (r'^(?P<slug>[\d\w\-_]+)/add/strip/$', views.add_strip, {}, "comics-webcomic-add_strip"),
    
    (r'^(?P<slug>[\d\w\-_]+)/archive/$', views.show_archive, {}, "comics-archive"),
    
    # shows strip
    (r'^(?P<slug>[\d\w\-_]+)/(?P<strip_id>\d+)-strip/$', views.show_webcomic, {}, "comics-strip"),
    
    # blog page
    (r'^(?P<slug>[\d\w\-_]+)/blog/(?P<pk>\d+)-(?P<blog_slug>[\d\w\-\_]+)/$', views.show_blog_page, {}, "comics-blog-page"),
)
