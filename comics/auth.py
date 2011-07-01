# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as auth_logout
from models import WebComic

def logout(request):
    auth_logout(request)
    comic_book = request.GET.get('book', None)
    if comic_book:
        webcomic = get_object_or_404(WebComic, pk=comic_book)
        return HttpResponseRedirect( webcomic.link() )
    else:
        return HttpResponseRedirect( reverse('comics.index') )