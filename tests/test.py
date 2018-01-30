from kubernetes import client, config
from taffrail.taffrail_client import MetricsClient

config.load_kube_config()
conf = client.Configuration()

metrics_client = MetricsClient(conf)
names = metrics_client.get_sources()
r1 = metrics_client.get_metrics_with_source('metrics-server')
r2 = metrics_client.get_metrics_with_source('metrics-api')
r3 = metrics_client.get_metrics_with_source('kube-state-metrics')
all = metrics_client.get_metrics()
print("done")