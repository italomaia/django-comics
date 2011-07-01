What is django-comics?
======================
Django comics is a simple webcomic publishing system. 

How to setup django-comics?
===========================
pip install -e git://github.com/italomaia/django-comics.git#egg=comics
then add to your installed apps: 'registration', 'django.contrib.markup', 'django.contrib.comments' and 'django.contrib.admin'.
Configure MEDIA_URL and STATIC_URL and your database. Your project urls.py should look somewhat like this:

    from django.conf import settings
    from django.conf.urls.defaults import patterns, include, url
    from django.contrib import admin
    admin.autodiscover()
    
    urlpatterns = patterns('',
        url(r'^accounts/', include('registration.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('mycomic.comics.urls')),
    )
    
    if settings.DEBUG:
        urlpatterns += patterns('django.views.static',
            (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'serve',
            {'document_root': settings.MEDIA_ROOT}),
        )

Now sync database and voilá! = ]
