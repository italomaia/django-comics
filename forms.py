# -*- coding: utf-8 -*-

#--- Framework Imports ---
from django import forms
from django.utils.translation import ugettext as _

##--- Application Imports ---
#from . import app_settings

from .models import WebComic, Strip

#from .fields import SafeHtmlField
from .widgets import ForumFileWidget

webcomic_image = WebComic._meta.get_field('image')
webcomic_thumb = WebComic._meta.get_field('thumbnail')

class EditWCForm(forms.ModelForm):
    image = forms.ImageField(label=webcomic_image.verbose_name,
                             help_text=webcomic_image.help_text,
                             widget=ForumFileWidget())
    thumbnail = forms.ImageField(label=webcomic_thumb.verbose_name,
                                 help_text=webcomic_thumb.help_text,
                                 widget=ForumFileWidget())
    class Meta: 
        model = WebComic
        fields = ('image', 'thumbnail', 'description', 'mature_flag')

strip_image = Strip._meta.get_field('image')
class EditStripForm(forms.ModelForm):
    image = forms.ImageField(label=strip_image.verbose_name,
                             help_text=strip_image.help_text,
                             widget=ForumFileWidget())
    class Meta:
        model = Strip
        fields = ('name', 'description', 'legend', 'image', 'tags', 'enable_comments')

#class WebComicForm(forms.ModelForm):
    
    
    #def clean_thumbnail(self):
        #data = self.cleaned_data["thumbnail"]
        #if isinstance( data, unicode ):
            ## no changes made...returning
            #return data
        
        #image_data = data.read()
        
        #from StringIO import StringIO
        #from PIL import Image
        
        ## validating thumbnail size
        #if len(image_data)/1024 > app_settings.THUMBNAIL_MAX_SIZE:
            #raise forms.ValidationError(_("Thumbnail's size is too big. Max is %(size)dkb") % {"size":app_settings.THUMBNAIL_MAX_SIZE})
        
        #return data
    
    #class Meta:
        #model = WebComic

