# part1/spark_query2.py — Part 1.4: Spark implementation of Query 2
# Compares in-database MongoDB Q2 vs Spark on same data
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time

# Part 1.4 — Spark Session
spark = SparkSession.builder.appName("ADM_Part1_Q2").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

users = spark.read.csv("data/users.csv", header=True, inferSchema=True)
trips = spark.read.csv("data/trips.csv", header=True, inferSchema=True)

# Part 1.4 — Query 2: trip count + avg duration per user using Spark
trips2 = trips.withColumn("dur_min",
    (F.unix_timestamp("end_time") - F.unix_timestamp("start_time")) / 60)

agg = trips2.groupBy("user_id").agg(
    F.count("id").alias("trip_count"),
    F.round(F.avg("dur_min"), 2).alias("avg_duration_min")
)

result = users.join(agg, users.id == agg.user_id, "left").drop("user_id")

t = time.time()
n = result.count()   # triggers Spark action
elapsed = round(time.time()-t, 3)

print(f"Spark Q2: {n} rows in {elapsed}s")
result.show(5)
spark.stop()