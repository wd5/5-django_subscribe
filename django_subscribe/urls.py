# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',    
    url(r'^add', add, name='add'),    
    url(r'^confirm', confirm, name='confirm'),
    url(r'^cancel', cancel, name='cancel'),
    
    url(r'^post', post, name='post'),
    )