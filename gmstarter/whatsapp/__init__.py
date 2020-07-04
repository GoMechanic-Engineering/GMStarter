import sys
from confluent_kafka import Producer
import datetime
from django.conf import settings
import json
import traceback

p = Producer(settings.KAFKA_CONFIG)

class WhatsappMessage:
    templateId = ""
    data = {}

    def __init__(self, templateId, data={}):
        self.templateId = templateId
        self.data = data
        self.send(templateId, data)

    def send(self, templateId, data):
        
        try:
            p.produce('whatsapp_message', key=settings.GM_SERVER_NAME, value=json.dumps(self.getFormattedArgs(templateId, data)).encode('utf-8'), callback=None)
        except Exception as e:
            try:
                p.produce('whatsapp_message', key=settings.GM_SERVER_NAME, value=json.dumps(self.getFormattedExceptionArgs(str(traceback.format_exc()))).encode('utf-8'), callback=None)
            except Exception as e1:
                print(str(traceback.format_exc()))

    def getFormattedArgs(self, templateId, data):
        return {'templateId' : templateId, 'data' : data, 'type' : 'message'}

    def getFormattedExceptionArgs(self, error):
        return {'type' : 'kafka_exception', 'time' : str(datetime.datetime.now()), 'info' : error}
