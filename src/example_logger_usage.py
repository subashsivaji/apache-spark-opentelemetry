# Databricks notebook source
# MAGIC %run ../config/set_logger

# COMMAND ----------

def edp_spark_reader_csv_v2(url, on_error_action, format = "csv", delimiter = "\t"):
  
  start_message = "Start reading file at path {0}".format(url)
  end_message = "End reading file at path {0}".format(url)
  
  exit_message = " ...| Exiting the notebook {0} | Exception logged to azure monitor | on_error_action = {1}".format(url, on_error_action)
  error_message = " ...| Failed for File {0} | Exception logged to azure monitor | on_error_action = {1}".format(url, on_error_action)
  
  try:
    logger.info(start_message)
    df = spark.read.format(format)\
              .option("header", "true")\
              .option("delimiter", delimiter)\
              .load(url)
    logger.info(end_message)
  except BaseException as e:
    logger.exception(e)
    
    if on_error_action == "exit":
      print(str(e))
      dbutils.notebook.exit(str(e) + exit_message)
    
    elif on_error_action == "error":
      print(str(e))
      raise Exception(str(e) + error_message)
  return(df)

# COMMAND ----------

file_path = "/mnt/edp1_prepare/NetSuite/ExchangeRate.txtxxxx"

df_exrate_01 = edp_spark_reader_csv_v2(url=file_path, on_error_action="exit")

# COMMAND ----------

df_exrate_01.count()
