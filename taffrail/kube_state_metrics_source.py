from prometheus_client.parser import text_string_to_metric_families
import json
import os
from .metrics import MetricsUtility

class KubeStateMetricsSource(object):
    enabled = False
    endpoint = {"KUBE_STATE_METRICS_NAME": "kube-state-metrics:http-metrics", "KUBE_STATE_METRICS_NAMESPACE": "kube-system", "KUBE_STATE_METRICS_PATH": "/metrics"}

    def __init__(self, kubernetes_client):
        self.name = "kube-state-metrics"
        self.api = kubernetes_client.CoreV1Api()
        self.__discover()

    def __discover(self):
        for env_var in self.endpoint:
            if os.environ.get(env_var) is not None:
                KubeStateMetricsSource.endpoint[env_var] = os.environ.get(env_var)
        
        try:
            self.api.connect_get_namespaced_service_proxy_with_path(KubeStateMetricsSource.endpoint['KUBE_STATE_METRICS_NAME'],
                KubeStateMetricsSource.endpoint['KUBE_STATE_METRICS_NAMESPACE'], KubeStateMetricsSource.endpoint['KUBE_STATE_METRICS_PATH'])
        except Exception as err:
            return

        self.enabled = True

    def get_metrics(self):
        metrics_list = []
        
        kube_state_metrics_response = self.api.connect_get_namespaced_service_proxy_with_path(KubeStateMetricsSource.endpoint['KUBE_STATE_METRICS_NAME'],
                                        KubeStateMetricsSource.endpoint['KUBE_STATE_METRICS_NAMESPACE'],
                                        KubeStateMetricsSource.endpoint['KUBE_STATE_METRICS_PATH'])
        
        if kube_state_metrics_response:
            for family in text_string_to_metric_families(kube_state_metrics_response):
                metrics_obj = MetricsUtility().to_object(family)
                metrics_list.append(metrics_obj)
        
        return KubeStateMetricsResponse(self.name, metrics_list)


class KubeStateMetricsResponse(object):
    def __init__(self, name, items):
        self.name = name
        self.items = items
    
    def to_dict(self):
        return KubeStateMetricsResponse(self.name, [ob.__dict__ for ob in self.items]).__dict__
