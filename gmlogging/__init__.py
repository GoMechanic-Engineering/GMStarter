import sys
from confluent_kafka import Producer
import datetime
from django.conf import settings
import json

p = Producer(settings.KAFKA_CONFIG)

class GMLogging:
    global_name = ""

    def __init__(self, global_name):
        self.global_name = global_name

    def print(self, *args):
        print(args)
        

        p.produce('print_logging', key=self.global_name, value=json.dumps(self.getFormattedArgs(args)).encode('utf-8'), callback=None)

    def getFormattedArgs(self, *args):
        value = {'type' : 'print', 'time' : str(datetime.datetime.now()), 'info' : {}}
        count = 0
        for arg in args:
            value['info']['arg'+str(count)] = str(arg)
            count += 1

        return value
