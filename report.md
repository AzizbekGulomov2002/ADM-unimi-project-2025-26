# ADM Project Report (2025/26)

This report summarizes the implementation choices and results for the city mobility data management project.  
The focus is on *why* each model was chosen and how queries behaved in practice.

## Project Scope

The platform manages:
- users
- stations
- trips
- events (`GPS`, `ERROR`, `BATTERY`, `DELAY`)

Implemented technologies:
- Relational DB: PostgreSQL
- Document DB: MongoDB
- Graph DB: Neo4j
- Distributed processing: Spark (DataFrames + GraphFrames)

---

## Part 1 — Relational vs Document Model

## 1.1 Data Modeling Choices

### PostgreSQL (normalized)
- Separate tables: `users`, `stations`, `trips`, `events`
- Foreign keys enforce consistency (`trips -> users/stations`, `events -> trips`)
- Good fit for structured joins and strict constraints

### MongoDB (hybrid with embedding)
- Collections: `users`, `stations`, `trips`
- `events` are embedded inside each `trip` document
- This was chosen to optimize Query 4 (find trips with at least one `ERROR` event), avoiding extra joins/lookups

Minimal sample (idea only):
```python
# PostgreSQL relation
trips(user_id -> users.id, start_station_id -> stations.id)

# MongoDB document
{
  "id": 101,
  "user_id": 3,
  "events": [{"type": "ERROR", "timestamp": "..."}]
}
```

## 1.2 Query Implementation (Q1–Q4)

Both PostgreSQL and MongoDB versions of the required queries were implemented:
1. trips + user + station names  
2. users + trip count + average duration  
3. stations + outgoing/incoming trip counts  
4. trips containing at least one `ERROR` event

Indexes were added in both systems to support frequent filters/grouping.

## 1.3 Performance Discussion (from benchmark runs)

Observed trend from your benchmark execution:
- **PostgreSQL** is consistently fast on Q1/Q2/Q4 and remains stable as data grows.
- **MongoDB** performs very well on aggregation-heavy Q2/Q3 and remains competitive on Q4 due to embedded events.
- **MongoDB Q1** is the slowest query in large datasets because of multiple `$lookup` stages.
- **PostgreSQL Q3** becomes expensive at large scale because it combines two trip joins per station.

Largest tested case (`u=50000, t=100000, e=5`) confirms this behavior.

## 1.4 Spark-based Query 2

Spark DataFrame implementation for Query 2 is provided in `part1/spark_query2.py`.
It computes duration in minutes, aggregates by `user_id`, and left-joins users.

Interpretation:
- Spark is useful when data is part of a distributed pipeline.
- For local/small-medium data, DB-native execution is usually faster due to Spark startup overhead.

---

## Part 2 — Graph Model

## 2.1 Graph Schema and Queries

Neo4j model:
- Nodes: `USER`, `TRIP`, `STATION`
- Edges: `PERFORMED`, `STARTS_AT`, `ENDS_AT`

Implemented queries:
1. stations reachable from a selected user via their trips
2. top-3 important stations by trip connectivity

Your run output shows both queries working correctly with realistic response times.

## 2.2 Spark GraphFrames

`part2/spark_graphframes.py` implements:
1. PageRank top-3 stations
2. connected components for station subgraph

This is aligned with assignment requirements for Spark graph analytics.

---

## Schema Evolution (BATTERY level field)

If `BATTERY` events require a new integer field `battery_level`:
- **PostgreSQL**: alter schema / nullable column / migration scripts
- **MongoDB**: add field only to relevant embedded event documents

Given current design, MongoDB offers easier incremental evolution for event payload changes.

---

## Partitioning and Replication Plan (short)

### Partitioning
- Partition by `user_id` favors user-centric queries (Q2 and graph traversals from user).
- Partition by `start_station_id` favors station-centric queries (Q3 and station importance).
- Recommended default: `user_id`, because many analytics start from users and it balances well for both Part 1 and Part 2.

### Replication (single leader, async)
- Reads from secondaries may be stale after recent writes.
- Inconsistency risk is higher for recent-trip/event queries.
- For strict correctness-sensitive reads, use primary/preferred-primary.

---

## Final Remarks

The implementation covers all required assignment parts with clear separation of responsibilities by file:
- data generation
- schema loading
- required queries
- benchmark comparison
- Spark extensions

Main practical result: use the database engine that matches query shape  
(joins/constraints -> PostgreSQL, flexible event evolution -> MongoDB, traversal -> Neo4j, distributed graph/data pipeline -> Spark).
