# apache-spark-opentelemetry
Send Apache Spark telemetry to Azure Monitor or other backend using OpenTelemetry/OpenCensus

# Apache Spark telemetry to Azure Monitor using OpenTelemetry

### **Overview**
**What is OpenTelemetry?**

OpenTelemetry provides the libraries, agents, and other components that you need to capture telemetry from your services so that you can better observe, manage, and debug them. Specifically, OpenTelemetry captures metrics, distributed traces, resource metadata, and logs (logging support is incubating now) from your applications and then sends this data to backend like Azure Monitor, Google Cloud Monitoring, Google Cloud Trace, Prometheus, Jaeger and [others](https://opentelemetry.io/registry/?s=exporter).

OpenTelemetry is a *Cloud Native Computing Foundation* Sandbox member, formed through a merger of the OpenTracing and OpenCensus projects.

> **Why we need OpenCensus?** OpenCensus will be superseded by OpenTelemetry in coming months. However, OpenTelemetry does not initially support **logging**, though it will be incorporated over time. So until then for **logging** purpose we still need to use OpenCensus libraries. [Announcing OpenTelemetry: the merger of OpenCensus and OpenTracing](https://cloudblogs.microsoft.com/opensource/2019/05/23/announcing-opentelemetry-cncf-merged-opencensus-opentracing/)


**Three types of telemetry**

Observability typically refers to telemetry produced by services and is often divided into three major verticals:

* **Tracing**, aka Distributed Tracing, provides insight into the full life cycles, aka traces, of requests to the system, allowing you to pinpoint failures and performance issues.
* **Metrics** provide quantitative information about processes running inside the system, including counters, gauges, and histograms.
* **Logging** provides insight into application-specific messages emitted by processes.

 
> Note: As of May 2020, out of 3 telemetry types - OpenTelemetry doesn't support Logging yet. So until then we have to use OpenCensus for logging. Once OpenTelemetry supports logging this repository and doc will be updated to use OpenTelemetry instead of OpenCensus.

These verticals are tightly interconnected. **Metrics** can be used to pinpoint, for example, a subset of misbehaving **traces**. **Logs** associated with those traces could help to find the root cause of this behaviour. And then new **metrics** can be configured, based on this discovery, to catch this issue earlier next time. Other verticals exist (continuous profiling, production debugging, etc.), however traces, metrics, and logs are the three most well adopted across the industry.

### **Things to consider**

- The minimum supported python version for OpenTelemetry is 3.7.3	
    - Code in this repo was tested on Databricks runtime 6.4 which supports python version 3.7.3
    - OpenTelemetry doesn't work on Databricks runtime 5.5 LTS, this runtime only supports python version 3.5.2	
- We have the ability to add custom dimensions to add more meaning and customised attributes to the logs.

### **Usage**

#### **How can we use OpenTelemetry/OpenCensus in Apache Spark?**

When working with Apache Spark applications especially if the codebase is pre-dominantly *pyspark* one of the ways to send application logs to Azure Monitor is using OpenTelemetry.

Following is the OpenTelemetry python azure monitor package. This implicitly installs opentelemetry-sdk and opentelemetry-api.

````python
pip install opentelemetry-azure-monitor
````

Following is the OpenCensus python azure monitor package.
````python
pip install opencensus-ext-azure
````
> Note: If using databricks, instead of pip install add the above PyPi libraries to databricks clusters.

#### **Define logger**
> *set_logger.py* uses azure key vault and databricks as an example. But with minor modifications this can be used in any apache spark application and can use any secret or key management tool.

Within this repository there is a script named [set_logger.py](https://github.com/subashsivaji/apache-spark-opentelemetry/blob/fe5b8af70f36d352ace26e8dbfc03b798aa3aa07/set_logger.py). This script encapsulates some of initialisation tasks that are needed to link Apache Spark/databricks and Azure Monitor such as,
- import necessary modules
- define OpenTelemetry azure monitor exporter
- link databricks and azure monitor using instrumentation key stored in azure key vault.
- add custom dimensions

set_logger can be a notebook which can be invoked in another databricks notebook via `%run` dbutils command. Or can be python function.

Once set_logger is defined we can use any [logger](https://docs.python.org/3.7/library/logging.html#logging.Logger) methods such as `logger.info`, `logger.warning`, `logger.exception`, `logger.critical` etc.

#### **Example logger usage**
Within this repository there is a script named [example_logger_usage.py](https://github.com/subashsivaji/apache-spark-opentelemetry/blob/fe5b8af70f36d352ace26e8dbfc03b798aa3aa07/example_logger_usage.py).

This invokes set_logger script/notebook and provides examples on how to logger methods.

Following is a example screenshot on how the logs would look like in Azure Monitor logs
:::image type="content" source="screenshot_azure_monitor_log_datarbicks.png" alt-text="":::

### **Reference**

[OpenCensus Python Azure Monitor README]( https://github.com/census-instrumentation/opencensus-python/tree/master/contrib/opencensus-ext-azure )

[OpenTelemetry Python Azure Monitor README](https://github.com/microsoft/opentelemetry-azure-monitor-python)