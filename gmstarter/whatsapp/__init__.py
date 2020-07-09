import sys
from confluent_kafka import Producer
import datetime
from django.conf import settings
import json
import traceback

p = Producer(settings.KAFKA_CONFIG)

class WhatsappMessage:
    phone = ""
    templateId = ""
    data = {}

    def __init__(self, phone, templateId, parameterData={}):
        self.phone = str(phone)
        self.templateId = str(templateId)
        self.parameterData = parameterData
        self.send(phone, templateId, parameterData)

    def send(self, phone, templateId, parameterData):
        try:
            p.produce('whatsapp_message', key=settings.GM_SERVER_NAME, value=json.dumps(self.getFormattedArgs(phone, templateId, parameterData)).encode('utf-8'), callback=None)
        except Exception as e:
            try:
                p.produce('whatsapp_message', key=settings.GM_SERVER_NAME, value=json.dumps(self.getFormattedExceptionArgs(str(traceback.format_exc()))).encode('utf-8'), callback=None)
            except Exception as e1:
                print(str(traceback.format_exc()))

    def getFormattedArgs(self, phone, templateId, parameterData):
        return {'templateId' : templateId, 'parameterData' : parameterData, 'type' : 'message', 'phone' : phone}

    def getFormattedExceptionArgs(self, error):
        return {'type' : 'kafka_exception', 'time' : str(datetime.datetime.now()), 'info' : error}
