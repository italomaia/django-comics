#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class ForumFileWidget(forms.FileInput):
    "Copy glued from admin widgets"
    def __init__(self, attrs={}):
        super(ForumFileWidget, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('<ul class="lista"><li>%s <a target="_blank" href="%s">%s</a></li><li>%s ' % \
                (_('Currently:'), value.url, value, _('Change:')))
            output.append(super(ForumFileWidget, self).render(name, value, attrs))
            output.append("</li></ul>")
        else:
            output.append(super(ForumFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))