# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class SubscriptionAdmin(admin.ModelAdmin):
   list_display = ('email', 'confirmation_code', 'date_created')
   ordering = ['-date_created']
   search_fields = ('email',)

admin.site.register(Subscription, SubscriptionAdmin)