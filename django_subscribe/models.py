# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5
from random import randint

from django.conf import settings
from django.db import models
from django.forms import ValidationError


class Subscription(models.Model):
    email = models.EmailField(verbose_name=u"Email")
    confirmation_code = models.CharField(verbose_name=u"Код подтверждения", max_length=32, null=True, blank=True, default=None)
    delete_code = models.CharField(verbose_name=u"Код удаления", max_length=32, null=True, blank=True, default=None)
    date_created = models.DateField(auto_now_add=True, verbose_name=u"Дата создания")

    def __unicode__(self):
        return self.email

    @classmethod
    def valid_emails(cls):
        return cls._default_manager.filter(confirmation_code__isnull=True)

    @classmethod
    def add(cls, email, auto_confirm=False):
        obj = cls(email=email)
        obj.fill_codes()
        if auto_confirm:
            obj.confirm(obj.confirmation_code)
        return obj

    def confirm(self, confirmation_code):
        if self.confirmation_code == confirmation_code:
            self.confirmation_code = None
            self.save()
        else:
            raise ValidationError('Wrong confirmation code')

    def cancel(self, delete_code):
        if self.delete_code == delete_code:
            self.delete()
        else:
            raise ValidationError('Wrong delete code')

    def fill_codes(self):
        def get_random():
            return md5(str(randint(1, 1000000000))).hexdigest()

        self.confirmation_code = get_random()
        self.delete_code = get_random()
        self.save()

    class Meta:
        verbose_name = u"Email"
        verbose_name_plural = u"Emails"
