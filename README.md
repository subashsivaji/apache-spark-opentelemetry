# Apache Spark telemetry to Azure Monitor using OpenTelemetry

### **Overview**

> **Note:** We previously used [AppInsights SDK for Python](https://github.com/microsoft/ApplicationInsights-Python) to send application logs from apache spark/databricks application. The reason to use OpenTelemetry/Opencensus is because [AppInsights SDK for Python](https://github.com/microsoft/ApplicationInsights-Python) is deprecated and is no longer maintained or supported by Microsoft.

**What is OpenTelemetry?**

OpenTelemetry provides the libraries, agents, and other components that you need to capture telemetry from your services so that you can better observe, manage, and debug them. Specifically, OpenTelemetry captures metrics, distributed traces, resource metadata, and logs (logging support is incubating now) from your applications and then sends this data to backend like Azure Monitor, Google Cloud Monitoring, Google Cloud Trace, Prometheus, Jaeger and [others](https://opentelemetry.io/registry/?s=exporter).

OpenTelemetry is a *Cloud Native Computing Foundation* Sandbox member, formed through a merger of the OpenTracing and OpenCensus projects. The project is contributed by Google, Microsoft and others.

> **Why we need OpenCensus?** OpenCensus will be superseded by OpenTelemetry in coming months. However, OpenTelemetry does not initially support **logging**, though it will be incorporated over time. So until then for **logging** purpose we still need to use OpenCensus libraries. [Announcing OpenTelemetry: the merger of OpenCensus and OpenTracing](https://cloudblogs.microsoft.com/opensource/2019/05/23/announcing-opentelemetry-cncf-merged-opencensus-opentracing/)


**Three types of telemetry**

Observability typically refers to telemetry produced by services and is often divided into three major verticals:

* **Logging** provides insight into application-specific messages emitted by processes.
* **Metrics** provide quantitative information about processes running inside the system, including counters, gauges, and histograms.
* **Tracing**, aka Distributed Tracing, provides insight into the full life cycles, aka traces, of requests to the system, allowing you to pinpoint failures and performance issues.

> Note: As of June 2020, out of 3 telemetry types - OpenTelemetry doesn't support Logging yet. So until then we have to use OpenCensus libraries for logging. Once OpenTelemetry supports logging, this repository and doc will be updated.

These verticals are tightly interconnected. **Metrics** can be used to pinpoint, for example, a subset of misbehaving **traces**. **Logs** associated with those traces could help to find the root cause of this behaviour. And then new **metrics** can be configured, based on this discovery, to catch this issue earlier next time. Other verticals exist (continuous profiling, production debugging, etc.), however traces, metrics, and logs are the three most well adopted across the industry.

### **Things to consider**

- The minimum supported python version for OpenTelemetry is 3.7.3	
    - Code in this repo was tested on Databricks runtime 6.4 which supports python version 3.7.3
    - OpenTelemetry doesn't work on Databricks runtime 5.5 LTS, this runtime only supports python version 3.5.2	
- We have the ability to add custom dimensions to add more meaning and customised attributes to the logs.

### **Usage**

#### **How can we use OpenTelemetry/OpenCensus in Apache Spark?**

Following is the [OpenTelemetry python azure monitor package](https://pypi.org/project/opentelemetry-azure-monitor/). This implicitly installs opentelemetry-sdk and opentelemetry-api.

````python
# using pip
pip install opentelemetry-azure-monitor
````
````python
# using databricks CLI
databricks libraries install --cluster-id "$($clusterId)" --pypi-package "opentelemetry-azure-monitor"
````

Following is the [OpenCensus python azure monitor package](https://pypi.org/project/opencensus-ext-azure/).
````python
# using pip
pip install opencensus-ext-azure
````
````python
# using databricks CLI
databricks libraries install --cluster-id "$($clusterId)" --pypi-package "opencensus-ext-azure"
````

#### **Define logger**
> *set_logger.py* uses azure key vault and databricks as an example. But with minor modifications this can be used in any apache spark application and can use any secret or key management tool.

Within this repository there is a script named [set_logger.py](src/set_logger.py). This script encapsulates some of initialisation tasks that are needed to link Apache Spark/Databricks and Azure Monitor such as,
- import necessary modules
- define OpenTelemetry azure monitor exporter
- link databricks and azure monitor using instrumentation key stored in azure key vault
- add custom dimensions

set_logger can be a notebook which can be invoked in another databricks notebook via `%run` dbutils command. Or can be python function.

Once set_logger is defined we can use any [logger](https://docs.python.org/3.7/library/logging.html#logging.Logger) methods such as `logger.info`, `logger.warning`, `logger.exception`, `logger.critical` etc. to define and send our application logs to Azure Monitor.

In Azure Monitor, application logs will be available in **traces** tables under application insight scope.
Metrics will be available in **customMetrics** tables under application insight scope.

#### **Example logger usage**
Within this repository there is a script named [example_logger_usage.py](src/example_logger_usage.py).

This invokes set_logger script/notebook and provides examples on how to logger methods.

Following is a example screenshot on how the logs would look like in Azure Monitor.
In the image spark_script, spark_version and cluster_id are custom dimensions that we defined in set_logger. We have the ability to filter the logs on specific custom dimension that we have defined either using *Kusto Query Language* or a filter in visualisation.

````sql
# sample kusto query language to query azure monitor
traces | union exceptions
| where timestamp between (datetime('2020-06-05 00:00:00') .. datetime('2020-06-05 10:00:00'))
| project timestamp, cloud_RoleName, message = iff(message != '', message, outerMessage), customDimensions.spark_script, customDimensions.lineNumber, severityLevel, itemType, type, problemId, customDimensions.cluster_id, customDimensions.spark_version
| order by timestamp desc
````

##### Example of all severity levels in Azure Monitor logs:
![](img/screenshot_azure_monitor_log_databricks.png)

##### Example of an exception in Azure Monitor logs:
![](img/screenshot_azure_monitor_log_exception.png)

Below is another view in Azure Monitor (under Application Insights failures), in case of any errors how the stack trace and error messages are logged into Azure Monitor. In the screenshot below we filter on custom dimension spark script.
![](img/screenshot_azure_monitor_appinsight_failures.png)

### **Reference**

[OpenCensus Python Azure Monitor README]( https://github.com/census-instrumentation/opencensus-python/tree/master/contrib/opencensus-ext-azure )

[OpenTelemetry Python Azure Monitor README](https://github.com/microsoft/opentelemetry-azure-monitor-python)

[OpenTelemetry documentation](https://opentelemetry.io/docs/)