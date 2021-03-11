import sys
from confluent_kafka import Producer
import datetime
from django.conf import settings
import json
import traceback

p = Producer(settings.KAFKA_CONFIG)

class GMKarixLogging:
    global_name = ""

    def __init__(self, global_name):
        self.global_name = global_name

    def print(self, *args):
        print(args)
        
        try:
            p.produce('karix_logging', key=self.global_name, value=json.dumps(self.getFormattedArgs(args)).encode('utf-8'), callback=None)
            p.flush()
        except Exception as e:
            try:
                p.produce('karix_logging', key=self.global_name, value=json.dumps(self.getFormattedExceptionArgs(args)).encode('utf-8'), callback=None)
                p.flush()
            except Exception as e1:
                print(str(traceback.format_exc()))

    def getFormattedArgs(self, *args):
        value = {'type' : 'karix', 'time' : str(datetime.datetime.now()), 'info' : {}}
        count = 0
        for arg in args:
            value['info']['arg'+str(count)] = str(arg)
            count += 1

        return value

    def getFormattedExceptionArgs(self, *args):
        value = {'type' : 'kafka_exception', 'time' : str(datetime.datetime.now()), 'info' : "exception"}
        return value
