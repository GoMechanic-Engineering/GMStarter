import sys
from confluent_kafka import Producer
import datetime
from django.conf import settings
import json
import traceback
import requests

p = Producer(settings.KAFKA_CONFIG)

class WhatsappMessage:
    phone = ""
    templateId = ""
    data = {}

    def __init__(self, phone, templateId, data={}, buttons={}):
        self.phone = str(phone)
        self.templateId = str(templateId)
        self.data = data
        self.send(phone, templateId, data)

    def send(self, phone, templateId, data):
        r = requests.post(url = "https://comms.gomechanic.app/api/v1/whatsapp/whatsapp-message-send", data = json.dumps(self.getFormattedArgs(phone, templateId, data)), headers={'Content-Type' : 'application/json'})
        print(r.json())
        # try:
        #     p.produce('whatsapp_message', key=settings.GM_SERVER_NAME, value=json.dumps(self.getFormattedArgs(phone, templateId, data)).encode('utf-8'), callback=None)
        # except Exception as e:
        #     try:
        #         p.produce('whatsapp_message', key=settings.GM_SERVER_NAME, value=json.dumps(self.getFormattedExceptionArgs(str(traceback.format_exc()))).encode('utf-8'), callback=None)
        #     except Exception as e1:
        #         print(str(traceback.format_exc()))

    def getFormattedArgs(self, phone, templateId, data):
        return {'templateId' : templateId, 'data' : data, 'type' : 'message', 'phone' : phone}

    def getFormattedExceptionArgs(self, error):
        return {'type' : 'kafka_exception', 'time' : str(datetime.datetime.now()), 'info' : error}
