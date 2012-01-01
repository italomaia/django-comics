# -*- coding: utf-8 -*-

#--- Python Imports ---
from os import path

#--- Framework Imports ---
from django.conf import settings

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404 as get_object

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext as _
from django.utils import simplejson as json

from django.contrib.auth.decorators import login_required

#--- App Imports ---
from . import app_settings
from models import WebComic, Strip, BlogPage
from forms import EditWCForm, EditStripForm

templates_dir= "comics"


def rp(template_name, ctx, request):
    return render_to_response(path.join(templates_dir, template_name), 
                              ctx, context_instance=RequestContext(request))


def show_webcomic(request, slug, strip_id=None, template_name="webcomic.html"):
    ctx = {}
    ctx["webcomic"] = get_object(WebComic, slug=slug)    
    ctx["blog_pages"]=ctx["webcomic"].blog_page_list.filter(published=True)
    
    if strip_id is not None:
        ctx["strip"] = get_object(Strip, pk=strip_id)
    else: ctx["strip"] = ctx["webcomic"].current_strip()
    
    return rp(template_name, ctx, request)


def show_archive(request, slug, template_name="archive.html"):
    ctx = {}
    ctx["webcomic"] = get_object(WebComic, slug=slug)
    return rp(template_name, ctx, request)


def show_blog_page(request, slug, page_id, template_name="blog_page.html"):
    ctx = {}
    ctx["webcomic"] = get_object(WebComic, pk=slug)
    ctx["blog_page"] = get_object(BlogPage, pk=page_id)
    return rp(template_name, ctx, request)


@login_required
def edit(request, slug, pk=None, template_name="edit.html"):
    ctx, Form={}, EditWCForm
    ctx["webcomic"] = get_object(WebComic, pk=slug)
    
    if request.user != ctx["webcomic"].owner:
        return HttpResponseForbidden("You can not do that.", 'plain/text')
    
    if pk is not None:
        ctx["strip"] = get_object(Strip, pk=pk)
        Form = EditStripForm
        instance = ctx["strip"]
    else: instance = ctx["webcomic"]
    
    if request.method=="POST":
        ctx["form"] = Form(request.POST, request.FILES, instance=instance)
        if ctx["form"].is_valid():
            return HttpResponseRedirect( ctx["form"].save().link() )
    ctx["form"] = Form(instance=instance)
    return rp(template_name, ctx, request)


@login_required
def add_strip(request, slug, template_name="edit.html"):
    ctx = {}
    ctx["webcomic"] = get_object(WebComic, pk=slug)
    
    if request.user != ctx["webcomic"].owner:
        return HttpResponseForbidden("You can not do that.", 'plain/text')
    
    if request.method=="POST":
        ctx["form"] = EditStripForm(request.POST, request.FILES)
        if ctx["form"].is_valid():
            instance = ctx["form"].save(commit=False)
            instance.webcomic = ctx["webcomic"]
            instance.save()
            return HttpResponseRedirect( instance.link() )
    else: ctx["form"] = EditStripForm()
    return rp(template_name, ctx, request)
