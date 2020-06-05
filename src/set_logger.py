# Databricks notebook source
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
import json
import datetime
import time

instrumentation_key = dbutils.secrets.get(scope = "secretscope-keyvault", key = "secret-appinsight-instrumentationkey")

## refer https://docs.python.org/3.7/library/logging.html#logging.getLogger
## if nothing is specified within getLogger() function the name of the root
## __name__ is the module’s name in the Python package namespace.
logger = logging.getLogger(__name__)

## refer https://docs.python.org/3.7/library/logging.html#logging.Logger.setLevel
## set logger level to DEBUG so that anything above this level such as INFO, WARNING, CRITICAL gets logged
logger.setLevel('DEBUG')

## define azure monitor exporter - provide instrumentation key
exporter = AzureLogHandler(
    connection_string='InstrumentationKey={0}'.format(instrumentation_key)
    )

## applicable only for databricks - a way to get notebook/script properties
notecontext = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())

## define a python callback function to add any custom properties to the logger
def custom_dimension(envelope):
    envelope.data.baseData.properties['spark_script'] = notecontext['extraContext']['notebook_path'],
    envelope.data.baseData.properties['cluster_id'] = notecontext['tags']['clusterId'],
    envelope.data.baseData.properties['spark_version'] = spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion"),
    envelope.tags['ai.cloud.role'] = 'pg-adb-28q' ## this will be cloud_RoleName in Azure monitor
    return True

## adding the custom dimension to the logger
exporter.add_telemetry_processor(custom_dimension)

## we have defined the log handler/exporter above - attach/add this to the logger
logger.addHandler(exporter)