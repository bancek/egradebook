from django import template
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.utils import simplejson

from infosys.models import Oseba
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def smart(string):
    """
    Displays text in right encoding (could be ascii or unicode).
    """
    try:
        return unicode(string)
    except:
        return smart_unicode(string)

@register.filter
def lpad(text, num):
    """
    Left padding with spaces for num places.
    
    Example::
    
        {{ forloop.counter|lpad:3 }}
    """
    
    text = unicode(text)
    
    return ' ' * (num - len(text)) + text

@register.filter
def lpad_force(text, num):
    """
    Left padding with &nbsp; chars for num places.
    
    Example::
    
        {{ forloop.counter|lpad_force:3 }}
    """
    
    text = unicode(text)
    
    return '&nbsp;' * (num - len(text)) + text

@register.filter
def format(string, formatstr):
    """
    Formats text.
    
    Example::
    
        {{ number|format:'%2f' }}
    """
    
    if string:
        return formatstr % string
    
    return string

@register.filter
def jsonify(data):
    json = simplejson.dumps(data)
    
    return mark_safe(json)

def get_user(obj):
    if isinstance(obj, User):
        return obj
    elif isinstance(obj, Oseba):
        return obj.uporabnik

@register.filter
def name(obj):
    """
    Displays user's name.
    
    Example::
        
        {{ request.user|name }}
    """
    
    user = get_user(obj)
    
    if user:
        return user.get_full_name()

@register.inclusion_tag('blocks/errors.html')
def form_errors(form):
    """
    Renders form errors using template blocks/errors.html
    
    Example::
    
        {% form_errors my_form %}
    
    """
    
    return dict(form=form)

@register.inclusion_tag('blocks/formfield.html')
def form_field( field, label):
    """
    Renders form field using template blocks/formfield.html.
    
    Example::
    
        {% form_fieled my_form.my_field 'My Field:' %}
    
    """
    
    return dict(field=field, label=label)
