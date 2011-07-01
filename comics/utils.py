#-*- coding:utf-8 -*-

class Link(object):
    def __init__(self, o):
        self.o=o
    def __unicode__(self):
        return repr(self)
    
    def __getattr__(self, name):
        if name in self.__dict__.keys():
            return self.__dict__.get(name)
        elif hasattr(self.o, name):
            return getattr(self.o, name)
        elif hasattr(repr(self), name):
            return getattr(repr(self), name)
        else:raise AttributeError()