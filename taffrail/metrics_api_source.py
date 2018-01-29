from kubernetes import client
from prometheus_client.parser import text_string_to_metric_families
import json
import metrics

class MetricsApiSource(object):
    enabled = False

    def __init__(self, kubernetes_config):
        self.name = "metrics-api"
        self.endpoint = kubernetes_config.host + "/metrics"
        self.config = kubernetes_config
        self.__discover()

    def __discover(self):
        self.rest_client = client.rest.RESTClientObject(self.config)

        try:
            kube_state_metrics_response = self.rest_client.GET(self.endpoint)
        except Exception as err:
            return

        kube_state_metrics_status = kube_state_metrics_response.status

        if kube_state_metrics_status is 200:
            self.enabled = True

    def get_metrics(self):
        metrics_list = []

        metrics_response = self.rest_client.GET(self.endpoint)
        
        if metrics_response.status is 200:
            for family in text_string_to_metric_families(metrics_response.data):
                metrics_obj = metrics.MetricsUtility().to_object(family)
                metrics_list.append(metrics_obj)
        
        return MetricsApiResponse(self.name, metrics_list)


class MetricsApiResponse:
    def __init__(self, name, items):
        self.name = name
        self.items = items