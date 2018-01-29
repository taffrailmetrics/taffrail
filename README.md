Taffrail: Kubernetes Metrics Aggregation for Python
===================================================

Taffrail is a python package that automatically discovers metrics providers in a Kubernetes cluster and exposes them via a simple interface.
You can easily add custom metrics providers as well as override existing metrics endpoints.

Installation
------------

Install taffrail using pip:

`pip install taffrail`

Usage
-----

Create the client:

```
from kubernetes import client, config
from taffrail_client import MetricsClient

config.load_kube_config()
conf = client.Configuration()

metrics_client = MetricsClient(conf)
```


### Get all available metrics:

`response = metrics_client.get_metrics()`

### Get all available sources:

`response = metrics_client.get_sources()`

### Get metrics for a specific source:

`response = metrics_client.get_metrics_with_source('metrics-api')`

### Custom kube-state-metrics endpoint

By default, taffrail will look for kube-state metrics endpoint at: /api/v1/namespaces/kube-system/services/kube-state-metrics:http-metrics/proxy/metrics.
To override with a custom endpoint simply set the KUBE-STATE-METRICS-PATH env var.

Example:

`$ export KUBE-STATE-METRICS-PATH="/api/v1/namespaces/default/services/kube-state-metrics:8080/proxy/metrics"`


Available Sources
-----------------

Currently, taffrail supports the following metrics providers:

* kube-state-metrics
* metrics-api
* metrics-server
