from kubernetes import client
from prometheus_client.parser import text_string_to_metric_families
import json
import os
import metrics

class KubeStateMetricsSource(object):
    enabled = False
    path_env_var = 'KUBE-STATE-METRICS-PATH'

    def __init__(self, kubernetes_config):
        self.name = "kube-state-metrics"
        self.endpoint = kubernetes_config.host + "/api/v1/namespaces/kube-system/services/kube-state-metrics:http-metrics/proxy/metrics"
        self.config = kubernetes_config
        self.__discover()

    def __discover(self):
        if os.environ.has_key(KubeStateMetricsSource.path_env_var):
            self.endpoint = self.config.host + os.environ['KUBE-STATE-METRICS-PATH']

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

        kube_state_metrics_response = self.rest_client.GET(self.endpoint)
        
        if kube_state_metrics_response.status is 200:
            for family in text_string_to_metric_families(kube_state_metrics_response.data):
                metrics_obj = metrics.MetricsUtility().to_object(family)
                metrics_list.append(metrics_obj)
        
        return KubeStateMetricsResponse(self.name, metrics_list)


class KubeStateMetricsResponse(object):
    def __init__(self, name, items):
        self.name = name
        self.items = items
    
    def to_dict(self):
        return KubeStateMetricsResponse(self.name, [ob.__dict__ for ob in self.items]).__dict__
