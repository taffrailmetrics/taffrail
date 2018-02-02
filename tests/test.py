from kubernetes import client, config
from taffrail.taffrail_client import MetricsClient
import requests

config.load_kube_config()
metrics_client = MetricsClient(client)
names = metrics_client.get_sources()
r = metrics_client.get_metrics_with_source('heapster')
all = metrics_client.get_metrics()
print("done")