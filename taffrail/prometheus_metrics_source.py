from prometheus_client.parser import text_string_to_metric_families
import json
import os
import metrics
import requests

class PrometheusMetricsSource(object):
    enabled = False
    endpoint = {"PROMETHEUS_SERVICE_NAME": "prom-prometheus-server:80", "PROMETHEUS_NAMESPACE": "default", "PROMETHEUS_PATH": "/metrics"}

    def __init__(self, kubernetes_client):
        self.name = "prometheus"
        self.api = kubernetes_client.CoreV1Api()
        self.__discover()

    def __discover(self):
        for env_var in self.endpoint:
            if os.environ.get(env_var) is not None:
                PrometheusMetricsSource.endpoint[env_var] = os.environ.get(env_var)
        
        try:
            self.api.connect_get_namespaced_service_proxy_with_path(PrometheusMetricsSource.endpoint['PROMETHEUS_SERVICE_NAME'],
                PrometheusMetricsSource.endpoint['PROMETHEUS_NAMESPACE'], PrometheusMetricsSource.endpoint['PROMETHEUS_PATH'])
        except Exception as err:
            return

        self.enabled = True

    def get_metrics(self):
        metrics_list = []
        
        prom_response = self.api.connect_get_namespaced_service_proxy_with_path(PrometheusMetricsSource.endpoint['PROMETHEUS_SERVICE_NAME'],
                                            PrometheusMetricsSource.endpoint['PROMETHEUS_NAMESPACE'],
                                            PrometheusMetricsSource.endpoint['PROMETHEUS_PATH'])
            
        if prom_response:
            for family in text_string_to_metric_families(prom_response):
                metrics_obj = metrics.MetricsUtility().to_object(family)
                metrics_list.append(metrics_obj)
                    
        return PrometheusResponse(self.name, metrics_list)


class PrometheusResponse(object):
    def __init__(self, name, items):
        self.name = name
        self.items = items
    
    def to_dict(self):
        return PrometheusResponse(self.name, [ob.__dict__ for ob in self.items]).__dict__
