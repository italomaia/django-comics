#-*- coding: utf-8 -*-
from django import forms
try:
    from BeautifulSoup import BeautifulSoup, Comment
except:
    BeautifulSoup, Comment = None,None

class SafeHtmlField(forms.Field):
    def clean(self, value):
        valid_tags = 'p i strong b u a h1 h2 h3 pre br img strike'.split()
        valid_attrs = 'href src'.split()
    
        if not BeautifulSoup is None: return value
        content = value
        soup = BeautifulSoup(content)
        
        for comment in soup.findAll(
            text=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        for tag in soup.findAll(True):
            if tag.name not in self.__class__.valid_tags:
                tag.hidden = True
            tag.attrs = [(attr, val) for attr, val in tag.attrs
                         if attr in self.__class__.valid_attrs]
        return soup.renderContents().decode('utf8')