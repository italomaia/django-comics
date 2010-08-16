# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

import utils

class DatedModel(models.Model):
    created_time = models.DateTimeField(_("Created time"), auto_now_add=True)
    modified_time = models.DateTimeField(_("Created time"), auto_now=True)
    
    class Meta: abstract=True

class BlogPage(DatedModel):
    "Webpage é uma página criada dinâmicamente pelo autor"
    
    class Meta:
        db_table = "comics_blogpage"
        ordering = ["created_time"]
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        unique_together = (("webcomic", "slug"),)
    
    webcomic = models.ForeignKey("WebComic", related_name="blog_page_list", editable=False)
    published = models.BooleanField(_("Published?"), default=False)
    slug = models.SlugField(editable=False)# used in the url make up
    title = models.CharField(_("Title"), max_length=100)
    content = models.TextField(_("Well, write down your thoughts"))
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(self, BlogPage).save(*args, **kwargs)
    
    def link(self):
        return reverse("comics-blog-page", args=(self.webcomic.slug, self.slug))
    get_absolute_url = link
    

class WebComic(DatedModel):
    """    
    Representa uma revistinha online do autor. 
    Possui nome algumas configurações como flag de conteúdo maduro
    """
    slug = models.SlugField(primary_key=True, editable=False)# used in the url make up
    name = models.CharField(_("What's the webcomic name?"), max_length=100, 
                            help_text=_("Name your baby!"))
    
    image = models.ImageField(_("Header Image"), upload_to="comics/images/%Y/%b/headers/",
                              help_text=_("This image goes at the top of the webpage") ) 
    
    thumbnail = models.ImageField(_("Logo"), blank=True, null=True,
                                  upload_to="comics/images/%Y/%b/headers/thumbnails/")
    
    owner = models.ForeignKey(User, related_name="comics",
                              verbose_name=_("Who's the artist behind the pencil?"))
    
    description = models.TextField(_("A few words about this webcomic..."),
                                   blank=True, default=None, null=True)
        
    mature_flag = models.BooleanField(_("May this webcomic contain mature content?"), default=False, 
                                      help_text=_("If true, a warn message will be showed.") )
    
    strips_count = models.PositiveIntegerField(default=0, editable=False)
    
    def __unicode__(self): return self.name
    
    def save(self, *args, **kargs):
        self.slug = slugify(self.name)
        super(WebComic, self).save(*args, **kargs)
    
    def link(self):
        class Link(utils.Link):
            def __repr__(self):
                return reverse("comics-webcomic", args=(self.slug, ))
            def edit(self):
                return reverse("comics-edit-webcomic", args=(self.slug, ))
            def add_strip(self):
                return reverse("comics-webcomic-add_strip", args=(self.slug, ))
        return Link(self)
    
    def first_strip(self):
        return self.strips.order_by('id')[0] # returns first added strip
    
    def current_strip(self): 
        try:
            return self.strips.latest() # returns last added strip
        except: return None
    
    get_absolute_url = link # alias
    
    class Meta:
        ordering = ['slug']
        db_table = "comics_webcomic"

class Strip(DatedModel):
    "Representa uma tirinha de uma revistinha do autor"
    next_strip = models.ForeignKey('Strip', null=True, blank=True, editable=False,
                            related_name="next", verbose_name=_("Next Strip"))
    prev_strip = models.ForeignKey('Strip', null=True, blank=True, editable=False,
                            related_name="prev", verbose_name=_("Previous Strip"))    
    
    number = models.PositiveIntegerField(default=1)
    webcomic = models.ForeignKey(WebComic, related_name="strips", 
                            verbose_name=_("Comic Book"))        
    name = models.CharField(_("Strip's name"), max_length=50, blank=True, null=True,
                            help_text=_("A title for the strip?") )
    
    description = models.TextField(_("Description"), blank=True, null=True)
    legend = models.CharField(max_length=255, blank=True, null=True, help_text=_("Accepts markdown"))
    
    image = models.ImageField(_("Strip Image"),  upload_to="comics/images/%Y/%b/comics/", 
                            help_text=_("Strip image showed to the viewer") ) 
    
    tags = models.CharField(_("Tags"), max_length=50, blank=True, null=True, 
                            help_text=_("Comma separeted (ex: subject, subject...") )
    
    enable_comments = models.BooleanField(_('Enable comments?'), default=False)
    
    def __unicode__(self):
        return "%s, strip %d-%s, %s" % (self.webcomic.name.capitalize(), 
                                        self.number,
                                        self.name or 'nameless', 
                                        self.created_time.strftime("%d/%m/%Y"))
    
    def link(self):
        class Link(utils.Link):
            def __repr__(self):
                return reverse("comics-strip", args=(self.webcomic.slug, self.id))
            def edit(self):
                return reverse("comics-edit-strip", args=(self.webcomic.slug, self.id))
        return Link(self)
    
    get_absolute_url = link # alias
    
    class Meta:
        ordering = ["-created_time"]
        get_latest_by = "created_time"
        db_table = "comics_strip"

# signals 

# updating next and prev links
def strip_update_links(sender, instance, created, *args, **kwargs):
    if created:
        webcomic = instance.webcomic        
        webcomic.strips_count = webcomic.strips.count()
        webcomic.save()
        
        try:
            last_strip = webcomic.strips.exclude(id__exact=instance.id).get(next_strip__isnull=True)
            instance.number = last_strip.number+1
            instance.prev_strip=last_strip
            last_strip.next_strip=instance
            instance.save()
            last_strip.save()
        except Strip.DoesNotExist, e:
            pass

signals.post_save.connect(strip_update_links, Strip, dispatch_uid="strip_update_links")
