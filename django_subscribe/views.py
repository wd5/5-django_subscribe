# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext, Context, loader
from django.conf import settings
from django import forms
from django.template import Context, loader

from models import Subscription

class EmailForm(forms.Form):
    email = forms.EmailField(label=u'Email')

class PostForm(forms.Form):
    message = forms.CharField(label=u'', error_messages={'required': u'Введите текст письма'},
                        widget=forms.Textarea(attrs={'rows':30, 'cols':80}))
    send = forms.BooleanField(label=u'Отправить', error_messages={'required': u'Подтвердите, что письмо готово к отправке'})


def render_to_response(request, template_name, context_dict={}):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context)


def add(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        if Subscription.objects.filter(email=form.cleaned_data['email']).count() > 0:
            return render_to_response(request, 'subscribe/message.html', {'message':u'Вы уже подписаны на нашу рассылку.'})
        
        else:
            s = Subscription(email=form.cleaned_data['email'])
            s.fill_codes()
            
            subject, content = process_template('subscribe/invitation.html', 
                                                {'subscription': s})
            send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [s.email], fail_silently=False)
            
            return render_to_response(request, 'subscribe/message.html', {'message':u'Вы успешно подписаны, проверьте свою почту.'})
    
    return render_to_response(request, 'subscribe/add.html', {'form':form})


def process_template(template, context):
    """ Обрабатывает шаблон, в котором первая строка считается заголовком """
    t = loader.get_template(template)
    c = Context(context)
    subject, content = t.render(c).split("\n", 1)
    return subject.strip(), content


def confirm(request):
    try:
        s = Subscription.objects.get(email=request.GET.get('email', ''))
        if not s.confirmation_code:
            return render_to_response(request, 'subscribe/message.html', {'message':u'Вы уже подтвердили ваш email. Все новости нашего сайта будут приходить на вашу почту.'})

        try:
            s.confirm(request.GET.get('code', ''))
            return render_to_response(request, 'subscribe/message.html', {'message':u'Вы подписаны на новости сайта. Спасибо за интерес к нам.'})
        except forms.ValidationError:
            return render_to_response(request, 'subscribe/message.html', {'message':u'Код подтверждения неправильный. Перейдите по ссылке, указанной в письме.'})
    
    except Subscription.DoesNotExist:
        return render_to_response(request, 'subscribe/message.html', {'message':u'Указанный email не найден в нашей базе.'})


def cancel(request):
    try:
        s = Subscription.objects.get(email=request.GET.get('email', ''))

        try:
            s.cancel(request.GET.get('code', ''))
            return render_to_response(request, 'subscribe/message.html', {'message':u'Вы успешно удалили свой email из нашего списка рассылки.'})
        except forms.ValidationError:
            return render_to_response(request, 'subscribe/message.html', {'message':u'Код подтверждения неправильный. Перейдите по ссылке, указанной в письме.'})
    
    except Subscription.DoesNotExist:
        return render_to_response(request, 'subscribe/message.html', {'message':u'Указанный email не найден в нашей базе.'})


def post(request):
    if not request.user.is_superuser:
        raise Http404

    if request.GET and request.GET.get('sent'):
        return render_to_response(request, 'subscribe/message.html', {'message':u'%s писем отправлено.' % request.GET.get('sent')})
    
    form = PostForm(request.POST)
    if request.POST and form.is_valid():
        subject, content = form.cleaned_data['message'].split("\n", 1)
        subject = subject.strip()
        content += u"\n\nЧтобы отписаться от рассылки, перейдите по ссылке\n\nhttp://perspektiva-ekb.ru/subscribe/cancel?email=%s&code=%s"
        count = 0
        for s in Subscription.valid_emails():
            send_mail(subject, content  % (s.email, s.delete_code), settings.DEFAULT_FROM_EMAIL, [s.email], fail_silently=False)
            count += 1
        return HttpResponseRedirect(reverse('post')+'?sent=%s' % count)
    else:
        return render_to_response(request, 'subscribe/post.html', {'form':form})
