import re
import unicodedata
import sqlparse
import inspect
from htmlentitydefs import name2codepoint
from datetime import datetime, timedelta

from django.db.models.query import QuerySet
from django.db.models.sql.query import Query
from django.utils.encoding import smart_unicode
from django.http import Http404
from django.shortcuts import get_object_or_404

def formatsql(data):
    sql = data
    
    if isinstance(data, QuerySet):
        sql = unicode(data.query)
    
    if isinstance(data, Query):
        sql = unicode(data)
    
    return sqlparse.format(sql, reindent=True, keyword_case='upper')

def printsql(data):
    print formatsql(data)

def cached_property(f):
    """returns a cached property that is calculated by function f"""
    def get(self):
        try:
            return self._property_cache[f]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[f] = f(self)
            return x
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x
        
    return property(get)

def slugify(s, entities=False, decimal=True, hexadecimal=True,
        instance=None, slug_field='slug', filter_dict=None):
    
    s = smart_unicode(s)
    
    #character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)
        
    #decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass
    
    #hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass
    
    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    
    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())
    
    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')
    
    slug = s
    
    if instance:
        if not slug:
            slug = 'new'
        
        slug = slug[:48]
        
        def get_query():
            query = instance._default_manager.filter(**{slug_field: slug})
            if filter_dict:
                query = query.filter(**filter_dict)
            if not inspect.isclass(instance) and instance.pk:
                query = query.exclude(pk=instance.pk)
            return query
        
        counter = 1
        
        while get_query():
            slug = '%s%d' % (s, counter)
            counter += 1
    
    return slug

def form_data_empty(form):
    for field in form.fields.keys():
        if form.data.get(form[field].html_name, None):
            return False
    
    return True

def not_none_or_404(obj):
    if obj is None:
        raise Http404
    
    return obj

def get_object_or_none(klass, *args, **kwargs):
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404:
        pass

def monthdelta(date, months):
    if date.month == 12:
        return datetime(date.year + 1, 1, 1)
    else:
        return datetime(date.year, date.month + 1, 1)

def months_range(start_date, end_date):
    start_date = datetime(start_date.year, start_date.month, 1)
    end_date = datetime(end_date.year, end_date.month, 1)
    
    cd = start_date
    
    while cd <= end_date:
        yield (cd, monthdelta(cd, 1) - timedelta(1))
        
        cd = monthdelta(cd, 1)
    