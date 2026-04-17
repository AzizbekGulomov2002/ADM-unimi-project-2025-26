# part1/benchmark.py — Part 1.2: Performance Comparison Table
# Run from project root: python part1/benchmark.py
import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import data.generate_data
import part1.setup_postgres  as pg_s
import part1.setup_mongodb   as mg_s
import part1.queries_postgres as pg_q
import part1.queries_mongodb  as mg_q

# Part 1.2 — Benchmark configurations
CONFIGS = [
    (1000,  10000,  0),
    (1000,  10000,  2),
    (1000,  10000,  5),
    (10000, 50000,  2),
    (50000, 100000, 5),
]

def bench(fn): t=time.time(); fn(); return round(time.time()-t, 3)

hdr = f"{'Config':<28} {'PG-Q1':>7} {'PG-Q2':>7} {'PG-Q3':>7} {'PG-Q4':>7} | {'MG-Q1':>7} {'MG-Q2':>7} {'MG-Q3':>7} {'MG-Q4':>7}"
print(hdr); print("-"*len(hdr))

for u, t, e in CONFIGS:
    label = f"u={u}, t={t}, e={e}"
    data.generate_data.gen(u, t, e)
    pg_s.create_schema()
    for tbl, f in [("users","data/users.csv"),("stations","data/stations.csv"),
                   ("trips","data/trips.csv"),("events","data/events.csv")]:
        pg_s.load(tbl, f)
    mg_s.load_all()

    pg = [bench(fn) for fn in [pg_q.q1, pg_q.q2, pg_q.q3, pg_q.q4]]
    mg = [bench(fn) for fn in [mg_q.q1, mg_q.q2, mg_q.q3, mg_q.q4]]

    print(f"{label:<28} " + " ".join(f"{v:>7}" for v in pg) + " | " + " ".join(f"{v:>7}" for v in mg))