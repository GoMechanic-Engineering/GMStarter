import sys
import datetime
from django.conf import settings
import json
import traceback
import requests

class Call:
    phones = []
    type = ""

    def __init__(self, phones, type):
        self.phones = phones
        self.type = str(type)
        self.send(phones, type)

    def send(self, phones, type):
        formattedArgs = self.getFormattedArgs(phones, type)
        r = requests.post(url = "https://comms.gomechanic.app/api/twilio/call", data = json.dumps(formattedArgs), headers={'Content-Type' : 'application/json'})

    def getFormattedArgs(self, phones, type):
        return {'type' : type, 'phones' : phones}

    def getFormattedExceptionArgs(self, error):
        return {'type' : 'kafka_exception', 'time' : str(datetime.datetime.now()), 'info' : error}
