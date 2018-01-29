from prometheus_client.parser import text_string_to_metric_families
from metrics_server_source import MetricsServerSource
from kube_state_metrics_source import KubeStateMetricsSource
from metrics_api_source import MetricsApiSource
import json

class MetricsClient(object):
    def __init__(self, kubernetes_config):
        if not kubernetes_config:
            raise Exception('kubernetes_config param cannot be null')
        else:
            self.config = kubernetes_config
            self.__load_sources()
    
    def __load_sources(self):
        self.sources = []
        self.sources.append(KubeStateMetricsSource(self.config))
        self.sources.append(MetricsServerSource(self.config))
        self.sources.append(MetricsApiSource(self.config))
    
    def get_sources(self):
        return [source.name for source in self.sources]

    def get_metrics_with_source(self, source_name):
        source = next((source for source in self.sources if source.enabled is True and source.name == source_name), None)

        if source:
            metrics = source.get_metrics()
            return metrics
        else:
            return None

    def get_metrics(self):
        response = {}
        response["items"] = []

        for source in self.sources:
            if source.enabled is True:
                metrics = source.get_metrics()
                response["items"].append(metrics)
        
        return response
