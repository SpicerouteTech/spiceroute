# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks Delta Batch Operations - Create Table
# MAGIC 
# MAGIC Databricks&reg; Delta allows you to read, write and query data in data lakes in an efficient manner.
# MAGIC 
# MAGIC ## Datasets Used
# MAGIC We will use online retail datasets from `/mnt/training/online_retail` 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Getting Started
# MAGIC 
# MAGIC You will notice that throughout this course, there is a lot of context switching between PySpark/Scala and SQL.
# MAGIC 
# MAGIC This is because:
# MAGIC * `read` and `write` operations are performed on DataFrames using PySpark or Scala
# MAGIC * table creates and queries are performed directly off Databricks Delta tables using SQL
# MAGIC 
# MAGIC Run the following cell to configure our "classroom."

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Setup

# COMMAND ----------

# MAGIC %md
# MAGIC Set up relevant paths.

# COMMAND ----------

inputPath = "/mnt/training/online_retail/data-001/data.csv"
genericDataPath = userhome + "/generic/customer-data/"
deltaDataPath = userhome + "/delta/customer-data/"
backfillDataPath = userhome + "/delta/backfill-data/"

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ###  READ CSV data then WRITE to Parquet / Databricks Delta
# MAGIC 
# MAGIC Read the data into a DataFrame. Since this is a CSV file, let Spark infer the schema from the first row by setting
# MAGIC * `inferSchema` to `true`
# MAGIC * `header` to `true`
# MAGIC 
# MAGIC Use overwrite mode so that it is not a problem to re-write data in case you end up running the cell again.
# MAGIC 
# MAGIC Partition on `Country` because there are only a few unique countries. 
# MAGIC 
# MAGIC More information on the how and why of partitioning is contained in the links at the bottom of this notebook.
# MAGIC 
# MAGIC Then write the data to Parquet and Databricks Delta.

# COMMAND ----------

from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col

rawDataDF = (spark.read 
  .option("inferSchema", "true") 
  .option("header", "true")
  .csv(inputPath) 
  .withColumn("InvoiceNo", col("InvoiceNo").cast(IntegerType()))
)

# write to generic dataset
rawDataDF.write.mode("overwrite").format("parquet").partitionBy("Country").save(genericDataPath)

# write to delta dataset
rawDataDF.write.mode("overwrite").format("delta").partitionBy("Country").save(deltaDataPath)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### CREATE Using Non-Databricks Delta Pipeline
# MAGIC 
# MAGIC Create a table called `customer_data` using `parquet` out of the above data.
# MAGIC 
# MAGIC <img alt="Caution" title="Caution" style="vertical-align: text-bottom; position: relative; height:1.3em; top:0.0em" src="https://files.training.databricks.com/static/images/icon-warning.svg"/> Notice how you MUST specify a schema and partitioning info!

# COMMAND ----------

spark.sql("""
    DROP TABLE IF EXISTS customer_data
  """)
spark.sql("""
    CREATE TABLE customer_data (
      InvoiceNo INTEGER,
      StockCode STRING,
      Description STRING,
      Quantity INTEGER,
      InvoiceDate STRING,
      UnitPrice DOUBLE,
      CustomerID INTEGER,
      Country STRING)
    USING parquet 
    OPTIONS (path = '{}' )
    PARTITIONED BY (Country)
  """.format(genericDataPath))

# COMMAND ----------

# MAGIC %md
# MAGIC Perform a simple `count` query to verify the number of records.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM customer_data

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <img alt="Caution" title="Caution" style="vertical-align: text-bottom; position: relative; height:1.3em; top:0.0em" src="https://files.training.databricks.com/static/images/icon-warning.svg"/> Wait, no results? 
# MAGIC 
# MAGIC What is going on here is a problem that stems from its Apache Hive origins.
# MAGIC 
# MAGIC It's the concept of
# MAGIC <b>schema on read</b> where data is applied to a plan or schema as it is pulled out of a stored location, rather than as it goes into a stored location.
# MAGIC 
# MAGIC This means that as soon as you put data into a data lake, the schema is unknown <i>until</i> you perform a read operation.
# MAGIC 
# MAGIC To remedy, you repair the table using `MSCK REPAIR TABLE`.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> Only after table repair is our count of customer data correct.
# MAGIC 
# MAGIC Schema on read is explained in more detail <a href="https://stackoverflow.com/a/11764519/53495#" target="_blank">in this article</a>.

# COMMAND ----------

# MAGIC %sql
# MAGIC MSCK REPAIR TABLE customer_data;
# MAGIC 
# MAGIC SELECT count(*) FROM customer_data

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### CREATE Using Databricks Delta Pipeline
# MAGIC 
# MAGIC Create a table called `customer_data_delta` using `DELTA` out of the above data.
# MAGIC 
# MAGIC The notation is:
# MAGIC > `CREATE TABLE <table-name>` <br>
# MAGIC   `USING DELTA` <br>
# MAGIC   `LOCATION <path-do-data> ` <br>
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> Notice how we do not have to specify partition columns.

# COMMAND ----------

spark.sql("""
  DROP TABLE IF EXISTS customer_data_delta
""")
spark.sql("""
  CREATE TABLE customer_data_delta 
  USING DELTA 
  LOCATION '{}' 
""".format(deltaDataPath))

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC Perform a simple `count` query to verify the number of records.
# MAGIC 
# MAGIC <img alt="Caution" title="Caution" style="vertical-align: text-bottom; position: relative; height:1.3em; top:0.0em" src="https://files.training.databricks.com/static/images/icon-warning.svg"/> Notice how the count is right off the bat; no need to worry about table repairs.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM customer_data_delta

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #### Metadata
# MAGIC 
# MAGIC Since we already have data backing `customer_data_delta` in place, 
# MAGIC the table in the Hive metastore automatically inherits the schema, partitioning, 
# MAGIC and table properties of the existing data. 
# MAGIC 
# MAGIC Note that we only store table name, path, database info in the Hive metastore,
# MAGIC the actual schema is stored in `_delta_logs`.
# MAGIC 
# MAGIC Metadata is displayed through `DESCRIBE DETAIL <tableName>`.
# MAGIC 
# MAGIC As long as we have some data in place already for a Databricks Delta table, we can infer schema.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL customer_data_delta

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Exercise 1
# MAGIC 
# MAGIC Read data in `outdoorSmallPath` with options:
# MAGIC * first row is the header
# MAGIC * infer schema from the header
# MAGIC 
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** Since `StockCode` looks numeric, you will need to convert `StockCode` explicitly to String. 
# MAGIC 
# MAGIC * Use this notation `withColumn("StockCode", col("StockCode").cast(StringType()))`

# COMMAND ----------

# TODO
from pyspark.sql.types import StringType
from pyspark.sql.functions import col

outdoorSmallPath = "/mnt/training/online_retail/outdoor-products/outdoor-products-small.csv"
backfillDF = (spark       
 .read          
 FILL_IN

# COMMAND ----------

# TEST - Run this cell to test your solution.
from pyspark.sql.types import StructField, StructType, StringType, DoubleType, IntegerType, DoubleType

expectedSchema = StructType([
   StructField("InvoiceNo", IntegerType(), True),
   StructField("StockCode", StringType(), True),
   StructField("Description", StringType(), True),
   StructField("Quantity", IntegerType(), True),
   StructField("InvoiceDate", StringType(), True),
   StructField("UnitPrice", StringType(), True),
   StructField("CustomerID", IntegerType(), True),
   StructField("Country", StringType(), True),
])

dbTest("Delta-02-schemas", set(expectedSchema), set(backfillDF.schema))

print("Tests passed!")

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Exercise 2
# MAGIC 
# MAGIC Create a Databricks Delta table `backfill_data_delta` backed by `backfillDataPath`.
# MAGIC 
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** 
# MAGIC * Don't forget to use overwrite mode just in case
# MAGIC * Partititon by `Country`

# COMMAND ----------

# TODO
(backfillDF
 .write
 .mode("overwrite")
 FILL_IN

spark.sql("""
   DROP TABLE IF EXISTS backfill_data_delta
 """)
spark.sql("""
   CREATE TABLE backfill_data_delta 
FILL_IN

# COMMAND ----------

# TEST - Run this cell to test your solution.
try:
  tableExists = (spark.table("backfill_data_delta") is not None)
except:
  tableExists = False
  
dbTest("Delta-02-backfillTableExists", True, tableExists)  

print("Tests passed!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 3
# MAGIC 
# MAGIC Count number of records from `backfill_data_delta` where the `Country` is `Sweden`.

# COMMAND ----------

# TODO
count = spark.sql("FILL IN").collect()[0][0]

# COMMAND ----------

# TEST - Run this cell to test your solution.
dbTest("Delta-L2-backfillDataDelta-count", 2925, count)
print("Tests passed!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC Using Databricks Delta to create tables is quite straightforward and you do not need to specify schemas.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Review Questions
# MAGIC 
# MAGIC **Q:** What is the Databricks Delta command to display metadata?<br>
# MAGIC **A:** Metadata is displayed through `DESCRIBE DETAIL tableName`.
# MAGIC 
# MAGIC **Q:** Where does the schema for a Databricks Delta data set reside?<br>
# MAGIC **A:** The table name, path, database info are stored in Hive metastore, the actual schema is stored in the `_delta_logs` directory.
# MAGIC 
# MAGIC **Q:** What is the general rule about partitioning and the cardinality of a set?<br>
# MAGIC **A:** We should partition on sets that are of small cardinality to avoid penalties incurred with managing large quantities of partition info meta-data.
# MAGIC 
# MAGIC **Q:** What is schema-on-read?<br>
# MAGIC **A:** It stems from Hive and roughly means: the schema for a data set is unknown until you perform a read operation.
# MAGIC 
# MAGIC **Q:** How does this problem manifest in Databricks assuming a `parquet` based data lake?<br>
# MAGIC **A:** It shows up as missing data upon load into a table in Databricks.
# MAGIC 
# MAGIC **Q:** How do you remedy this problem in Databricks above?<br>
# MAGIC **A:** To remedy, you repair the table using `MSCK REPAIR TABLE` or switch to Databricks Delta!

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC 
# MAGIC Start the next lesson, [Append]($./03-Append).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Additional Topics & Resources
# MAGIC 
# MAGIC * <a href="https://docs.azuredatabricks.net/delta/delta-batch.html" target="_blank">Table Batch Read and Writes</a>
# MAGIC * <a href="https://en.wikipedia.org/wiki/Partition_(database)#" target="_blank">Database Partitioning</a>