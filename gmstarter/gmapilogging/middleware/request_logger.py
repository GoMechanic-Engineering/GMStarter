from django.conf import settings
from confluent_kafka import Producer
from django.utils.deprecation import MiddlewareMixin
import datetime
import os
import uuid
from time import strftime
import json
import traceback


p = Producer(settings.KAFKA_CONFIG)
p_key = settings.GM_SERVER_NAME


class GMLoggerMiddleware(MiddlewareMixin):
    """
    Transmits all requests' data to Kafka as a simple string.
    !Attention: Demonstration purpose only!
    """

    def process_request(self, request):
        curr_time = datetime.datetime.utcnow()
        request._request_start_time = curr_time
        request._request_id = str(uuid.uuid4())
        # value = {'path' : str(request.path), 'time' : str(curr_time), 'request_id' : request._request_id, 'info' : self.get_request_information(request)}
        value = {'type' : 'request', 'path' : str(request.path), 'time' : str(curr_time), 'request_id' : request._request_id, 'info' : self.get_request_information(request)}
        p.produce('request_logging', key=p_key, value=json.dumps(value).encode('utf-8'), callback=None)
        # p.produce('request_logging', value="testiing11", callback=None)
        # self.audit_logger.info('Got Request for the API %s at time %s.Generated request id is %s. Request data is %s.\n',
        #                        request.path, curr_time, request._request_id, self.get_request_information(request))

    def process_response(self, request, response):
        curr_time = datetime.datetime.utcnow()
        diff = curr_time - request._request_start_time
        try:
            res_content = response.content.decode('UTF-8')
        except:
            res_content = response.content
        value = {'type' : 'response', 'path' : str(request.path), 'time_diff' : str(diff.total_seconds()), 'request_id' : request._request_id, 
            'info' : str(res_content), 'status' : response.status_code}
        p.produce('request_logging', key=p_key, value=json.dumps(value).encode('utf-8'), callback=None)
        # self.metric_logger.info('%s sec elapsed in processing API %s request with id %s. \nResponse %s \n', diff.total_seconds(),
        #                         request.path, request._request_id,res_content)
        return response

    def get_request_information(self, request):
        request_information = dict()
        request_information['data'] = str(request.GET) or str(request.POST) or str(request.body)
        request_information['headers'] = str(request.headers)
        request_information['meta_data'] = str(request.META)
        request_information['cookies'] = str(request.COOKIES)
        return request_information

    def process_exception(self, request, exception):
        curr_time = datetime.datetime.utcnow()
        diff = curr_time - request._request_start_time
        
        # print traceback.format_exc()
        value = {'type' : 'exception', 'path' : str(request.path), 'time_diff' : str(diff.total_seconds()), 'request_id' : request._request_id, 
            'info' : str(traceback.format_exc()), 'status' : 1000}
        p.produce('request_logging', key=p_key, value=json.dumps(value).encode('utf-8'), callback=None)
        
        