# part2/spark_graphframes.py — Part 2.2: Spark GraphFrames
# PageRank on stations + Connected Components of stations subgraph
from pyspark.sql import SparkSession
from graphframes import GraphFrame
import time

# Part 2.2 — Spark + GraphFrames setup
spark = SparkSession.builder \
    .appName("ADM_GraphFrames") \
    .config("spark.jars.packages","graphframes:graphframes:0.8.3-spark3.5-s_2.12") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

stations = spark.read.csv("data/stations.csv", header=True, inferSchema=True)
trips    = spark.read.csv("data/trips.csv",    header=True, inferSchema=True)

# Vertices = stations | Edges = start_station → end_station per trip
vertices = stations.selectExpr("CAST(id AS STRING) AS id", "name", "city")
edges    = trips.selectExpr(
    "CAST(start_station_id AS STRING) AS src",
    "CAST(end_station_id   AS STRING) AS dst"
)
g = GraphFrame(vertices, edges)

# Part 2.2 — Q1: PageRank — top 3 most important stations
print("\n=== PageRank: Top 3 Stations ===")
t = time.time()
pr = g.pageRank(resetProbability=0.15, maxIter=5)
pr.vertices.orderBy("pagerank", ascending=False).limit(3) \
   .select("id","name","city","pagerank").show()
print(f"Time: {round(time.time()-t, 2)}s")

# Part 2.2 — Q2: Connected Components of stations subgraph
print("\n=== Connected Components ===")
spark.sparkContext.setCheckpointDir("/tmp/spark_ckpt")
t = time.time()
cc = g.connectedComponents()
cc.groupBy("component").count().orderBy("count", ascending=False).show()
print(f"Time: {round(time.time()-t, 2)}s")

spark.stop()