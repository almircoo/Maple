#!/usr/bin/env python
# encoding: utf-8


import logging
import os
import random
import string
import uuid
from hashlib import sha256

import bleach
import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.templatetags.static import static

# generate hash for validate server <--> user
def get_sha256(str):
    m = sha256(str.encode('utf-8'))
    return m.hexdigest()

# Cache decorator
def cache_decorator(expiration=3 * 60):
    def wrapper(func):
        def news(*args, **kwargs):
            try:
                view = args[0]
                key = view.get_cache_key()
            except:
                key = None
            if not key:
                unique_str = repr((func, args, kwargs))

                m = sha256(unique_str.encode('utf-8'))
                key = m.hexdigest()
            value = cache.get(key)
            if value is not None:
                # logger.info('cache_decorator get cache:%s key:%s' % (func.__name__, key))
                if str(value) == '__default_cache_value__':
                    return None
                else:
                    return value
            else:
                logger.debug(
                    'cache_decorator set cache:%s key:%s' %
                    (func.__name__, key))
                value = func(*args, **kwargs)
                if value is None:
                    cache.set(key, '__default_cache_value__', expiration)
                else:
                    cache.set(key, value, expiration)
                return value

        return news

    return wrapper

# Cache expiration
def expire_view_cache(path, servername, serverport, key_prefix=None):
    '''
    Refresh view cache
    :param path:url path
    :param servername:host
    :param serverport:port
    :param key_prefix:prefix
    :return:Whether it was successful or not
    '''
    from django.http import HttpRequest
    from django.utils.cache import get_cache_key

    request = HttpRequest()
    request.META = {'SERVER_NAME': servername, 'SERVER_PORT': serverport}
    request.path = path

    key = get_cache_key(request, key_prefix=key_prefix, cache=cache)
    if key:
        logger.info('expire_view_cache:get key:{path}'.format(path=path))
        if cache.get(key):
            cache.delete(key)
        return True
    return False

# Current site settings
@cache_decorator()
def get_current_site():
    site = Site.objects.get_current()
    return site

def send_email(emailto, title, content):
    from djangoblog.blog_signals import send_email_signal
    send_email_signal.send(
        send_email.__class__,
        emailto=emailto,
        title=title,
        content=content)

# Gnerate code 
def generate_code() -> str:
    """Generate random number verification code"""
    return ''.join(random.sample(string.digits, 6))

# Delete loggin cache
