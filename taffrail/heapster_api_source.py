from kubernetes import client
from prometheus_client.parser import text_string_to_metric_families
import json
from .metrics import MetricsUtility
import os

class HeapsterApiSource(object):
    enabled = False
    endpoint = {"HEAPSTER_NAME": "heapster", "HEAPSTER_NAMESPACE": "kube-system", "HEAPSTER_PATH": "/metrics"}

    def __init__(self, kubernetes_client):
        self.name = "heapster"
        self.client = kubernetes_client.CoreV1Api()
        self.__discover()

    def __discover(self):
        for env_var in self.endpoint:
            if os.environ.get(env_var) is not None:
                HeapsterApiSource.endpoint[env_var] = os.environ.get(env_var)

        try:
            self.client.connect_get_namespaced_service_proxy_with_path(HeapsterApiSource.endpoint['HEAPSTER_NAME'],
                HeapsterApiSource.endpoint['HEAPSTER_NAMESPACE'], HeapsterApiSource.endpoint['HEAPSTER_PATH'])
        except Exception as err:
            return

        self.enabled = True

    def get_metrics(self):
        metrics_list = []

        metrics_response = self.client.connect_get_namespaced_service_proxy_with_path(HeapsterApiSource.endpoint['HEAPSTER_NAME'],
                HeapsterApiSource.endpoint['HEAPSTER_NAMESPACE'], HeapsterApiSource.endpoint['HEAPSTER_PATH'])
        
        if metrics_response:
            for family in text_string_to_metric_families(metrics_response):
                metrics_obj = MetricsUtility().to_object(family)
                metrics_list.append(metrics_obj)
        
        return HeapsterMetrics(self.name, metrics_list)


class HeapsterMetrics(object):
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def to_dict(self):
        return HeapsterMetrics(self.name, [ob.__dict__ for ob in self.items]).__dict__
    