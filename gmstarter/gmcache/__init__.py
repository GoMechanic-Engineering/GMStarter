from django.conf import settings
import sys
from django.db.models import Model
from django.apps import apps
import json
import functools


class GMCache:
    REDIS = None

    def __init__(self):
        self.REDIS = settings.REDIS

    def set(self, key, value=None, weeks=0, days=0, hours=0, minutes=0, seconds=0, nExists=False, xExists=False):
        expiry = (weeks*7*24*60*60) + (days*24*60*60) + (hours*60*60) + (hours*60*60) + (minutes*60) + seconds
        if expiry != 0:
            self.REDIS.set(key, value, ex=expiry, nx=nExists, xx=xExists)
        else:
            self.REDIS.set(key, value, nx=nExists, xx=xExists)
    
    def get(self, key):
        return self.REDIS.get(key)

    def delete(self, *names):
        return self.REDIS.delete(names)

    def setJson(self, key, value, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        expiry = (weeks*7*24*60*60) + (days*24*60*60) + (hours*60*60) + (hours*60*60) + (minutes*60) + seconds
        self.REDIS.execute_command('JSON.SET', key, '.', json.dumps(value))
        if expiry != 0:
            self.REDIS.expire(key, expiry)

    def getJson(self, key):
        return json.loads(self.REDIS.execute_command('JSON.GET', key))

    def expire(self, key, expiry):
        self.REDIS.expire(key, expiry)

    def expireat(self, key, when):
        self.REDIS.expireat(key, when)

    def setURLResponse(self, request, value=None, weeks=0, days=0, hours=0, minutes=0, seconds=0, nExists=False, xExists=False):
        expiry = (weeks*7*24*60*60) + (days*24*60*60) + (hours*60*60) + (hours*60*60) + (minutes*60) + seconds
        key = request.path.replace('/','-*-') + '-*-'.join([*list(functools.reduce(lambda x, y: x + y, sorted(request.query_params.items())))])
        # if expiry != 0:
        #     self.REDIS.set(key, value, ex=expiry, nx=nExists, xx=xExists)
        # else:
        #     self.REDIS.set(key, value, nx=nExists, xx=xExists)
        self.REDIS.execute_command('JSON.SET', key, '.', json.dumps(value))
        if expiry != 0:
            self.REDIS.expire(key, expiry)

    def getURLResponse(self, request):
        key = request.path.replace('/','-*-') + '-*-'.join([*list(functools.reduce(lambda x, y: x + y, sorted(request.query_params.items())))])
        return self.REDIS.get(key)