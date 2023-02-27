# Databricks notebook source
# MAGIC %run ../silver/transform_to_scd2

# COMMAND ----------

source_dataset_df = spark.read.format("delta").load(input_path+"bronze_"+dbutils.widgets.get("source_dataset"))
transform_to_scd2(source_dataset_df, "prod")

# COMMAND ----------

# MAGIC %run ../setup/generate_retail_data

# COMMAND ----------

generate_customer_data_day_2()

# COMMAND ----------

# MAGIC %run ../bronze/load_data_into_bronze

# COMMAND ----------

# Set the target location for the delta table
target_path = f"/FileStore/{username}_bronze_db/"

load_data_to_bronze(dbutils.widgets.get("source_dataset"), target_path)

# COMMAND ----------

source_dataset_df = spark.read.format("delta").option("readChangeFeed", "true") \
  .option("startingVersion", 2) \
  .load(input_path+"bronze_"+dbutils.widgets.get("source_dataset"))

transform_to_scd2(source_dataset_df, "prod")