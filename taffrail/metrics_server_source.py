from kubernetes import client
from collections import namedtuple
import metrics
import json

class MetricsServerSource(object):
    enabled = False
    resource_paths = ['/nodes', '/pods']

    def __init__(self, kubernetes_config):
        self.name = "metrics-server"
        self.endpoint = kubernetes_config.host + "/apis/metrics.k8s.io/v1beta1"
        self.config = kubernetes_config
        self.__discover()

    def __discover(self):
        self.rest_client = client.rest.RESTClientObject(self.config)
        
        try:
            metrics_server_response = self.rest_client.GET(self.endpoint)
        except Exception as err:
            return

        metrics_server_status = metrics_server_response.status

        if metrics_server_status is 200:
            self.enabled = True

    def get_metrics(self):
        items = []

        for path in self.resource_paths:
            response = self.rest_client.GET(self.endpoint + path)
            
            if response.status is 200:
                json_dict = json.loads(response.data)
                metrics_obj = metrics.MetricsUtility().to_object(json_dict)
                items.append(metrics_obj)

        return MetricsServerResponse(self.name, items)


class MetricsServerResponse:
    def __init__(self, name, items):
        self.name = name
        self.items = items
