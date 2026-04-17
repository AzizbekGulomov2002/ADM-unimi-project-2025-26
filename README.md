# ADM-project-2025-26

City mobility data management project for Advanced Data Management (a.y. 2025/2026).

GitHub repository: [AzizbekGulomov2002/ADM-project-2025-26](https://github.com/AzizbekGulomov2002/ADM-project-2025-26.git)

## Project Structure

- `data/generate_data.py` -> synthetic dataset generator
- `part1/setup_postgres.py` -> create PostgreSQL schema + load CSV
- `part1/queries_postgres.py` -> Part 1 PostgreSQL queries (Q1-Q4)
- `part1/setup_mongodb.py` -> create/load MongoDB collections
- `part1/queries_mongodb.py` -> Part 1 MongoDB queries (Q1-Q4)
- `part1/benchmark.py` -> benchmark table (PostgreSQL vs MongoDB)
- `part1/spark_query2.py` -> Spark implementation of Part 1 Query 2
- `part2/setup_neo4j.py` -> create/load Neo4j graph model
- `part2/queries_neo4j.py` -> Part 2 Neo4j queries
- `part2/spark_graphframes.py` -> GraphFrames (PageRank + connected components)
- `report.md` -> concise project report aligned with assignment structure
- `requirements.txt` -> pinned Python packages for `pip install -r`

## Requirements

- Python 3.10+ (tested with 3.13 locally)
- PostgreSQL (running locally)
- MongoDB (running locally)
- Neo4j (running locally, Bolt enabled)
- Java JDK 8+ (required for Spark/PySpark)

## Python packages

Install inside a virtual environment from the project root:

```bash
python3 -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Package summary (see `requirements.txt` for versions):

| Package | Used for |
|---------|----------|
| `psycopg2-binary` | PostgreSQL (`part1/setup_postgres.py`, `part1/queries_postgres.py`) |
| `pymongo` | MongoDB (`part1/setup_mongodb.py`, `part1/queries_mongodb.py`) |
| `neo4j` | Neo4j driver (`part2/setup_neo4j.py`, `part2/queries_neo4j.py`) |
| `pyspark` | Spark DataFrames (`part1/spark_query2.py`, `part2/spark_graphframes.py`) |
| `graphframes` | GraphFrames API (`part2/spark_graphframes.py`) |
| `matplotlib` | Plots (`generate_plots.py`, optional) |

## Database Connection Notes

Current scripts expect local defaults:
- PostgreSQL: db `adm_db`, user/password from script (or `.env` prepared in project root)
- MongoDB: default local `mongodb://localhost:27017`
- Neo4j: `bolt://localhost:7687` with configured credentials

## Recommended Run Order

From project root:

### 1) Generate default data
```bash
python3 data/generate_data.py
```

### 2) PostgreSQL setup + load
```bash
python3 part1/setup_postgres.py
```

### 3) MongoDB setup + load
```bash
python3 part1/setup_mongodb.py
```

### 4) Run Part 1 queries
```bash
python3 part1/queries_postgres.py
python3 part1/queries_mongodb.py
```

### 5) Run benchmark (Part 1 comparison)
```bash
python3 part1/benchmark.py
```

### 6) Neo4j setup + queries (Part 2)
```bash
python3 part2/setup_neo4j.py
python3 part2/queries_neo4j.py
```

### 7) Spark tasks (optional but required for assignment Spark parts)
```bash
python3 part1/spark_query2.py
python3 part2/spark_graphframes.py
```

If Spark fails with Java runtime error, install JDK and re-run.

## PostgreSQL Quick Start (local)

Example using `psql`:

```bash
createdb adm_db
psql -d adm_db -c "SELECT version();"
```

Then run:

```bash
python3 part1/setup_postgres.py
```

This script drops/recreates tables and loads CSV files.

## Report

Use `report.md` as the main technical narrative for submission draft.  
It is structured by assignment parts, with limited code snippets and stronger explanation of implementation choices/results.
