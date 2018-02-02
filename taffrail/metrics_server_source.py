from kubernetes import client
from collections import namedtuple
import requests
import urllib3
import metrics
import json
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MetricsServerSource(object):
    enabled = False
    resource_paths = ['/nodes', '/pods']
    endpoint = "/apis/metrics.k8s.io/v1beta1"
    
    def __init__(self, kubernetes_client):
        self.name = "metrics-server"
        self.config = kubernetes_client.Configuration()
        self.__discover()

    def __discover(self):
        try:
            response = requests.get(self.config.host + self.endpoint, headers=self.config.api_key, verify=False, cert=self.config.cert_file)
            if response.status_code is not 200:
                return
        except Exception as err:
            return

        self.enabled = True

    def get_metrics(self):
        items = []
        dict_obj = {}
        dict_obj['name'] = self.name
        dict_obj['items'] = []

        for path in self.resource_paths:
            response = requests.get(self.config.host + self.endpoint + path, headers=self.config.api_key, verify=False, cert=self.config.cert_file)
            
            if response.status_code is 200:
                json_dict = json.loads(response.content)
                dict_obj['items'].append(json_dict)
                metrics_obj = metrics.MetricsUtility().to_object(json_dict)
                items.append(metrics_obj)    

        return MetricsServerResponse(self.name, items, dict_obj)


class MetricsServerResponse(object):
    def __init__(self, name, items, dict_obj):
        self.name = name
        self.items = items
        self.dict = dict_obj

    def to_dict(self):
        return self.dict
