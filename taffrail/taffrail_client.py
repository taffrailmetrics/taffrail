from prometheus_client.parser import text_string_to_metric_families
from metrics_server_source import MetricsServerSource
from kube_state_metrics_source import KubeStateMetricsSource
from heapster_api_source import HeapsterApiSource
import json

class MetricsClient(object):
    def __init__(self, kubernetes_client):
        if not kubernetes_client:
            raise Exception('kubernetes_client param cannot be null')
        else:
            self.client = kubernetes_client
            self.__load_sources()
    
    def __load_sources(self):
        self.sources = []
        self.sources.append(KubeStateMetricsSource(self.client))
        self.sources.append(MetricsServerSource(self.client))
        self.sources.append(HeapsterApiSource(self.client))
    
    def get_sources(self):
        return [source.name for source in self.sources]

    def get_metrics_with_source(self, source_name):
        source = next((source for source in self.sources if source.enabled is True and source.name == source_name), None)

        if source:
            metrics = source.get_metrics()
            return metrics
        else:
            return None

    def get_metrics(self, as_dict = False):
        response = {}
        response["items"] = []

        for source in self.sources:
            if source.enabled is True:
                metrics = source.get_metrics()
                
                if as_dict is True:
                    metrics = metrics.to_dict()
                    
                response["items"].append(metrics)
        
        return response
