# -*- coding: utf-8 -*-

#--- Framework Imports ---
from django import forms
from django.utils.translation import ugettext as _

##--- Application Imports ---
#from . import app_settings

from .models import WebComic, Strip

from django.contrib.admin.widgets import AdminFileWidget

webcomic_image = WebComic._meta.get_field('image')
webcomic_thumb = WebComic._meta.get_field('thumbnail')


class EditWCForm(forms.ModelForm):
    image = forms.ImageField(label=webcomic_image.verbose_name, help_text=webcomic_image.help_text, widget=AdminFileWidget())
    thumbnail = forms.ImageField(label=webcomic_thumb.verbose_name, help_text=webcomic_thumb.help_text, widget=AdminFileWidget())
    
    class Meta:
        model = WebComic
        fields = ('image', 'thumbnail', 'description', 'mature_flag')


strip_image = Strip._meta.get_field('image')


class EditStripForm(forms.ModelForm):
    image = forms.ImageField(label=strip_image.verbose_name, help_text=strip_image.help_text, widget=AdminFileWidget())
    
    class Meta:
        model = Strip
        fields = ('name', 'legend', 'image', 'tags', 'enable_comments')
