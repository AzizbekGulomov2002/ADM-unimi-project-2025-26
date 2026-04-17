# part2/queries_neo4j.py — Part 2.1: Neo4j Queries
from neo4j import GraphDatabase
import time

URI = "bolt://localhost:7687"; AUTH = ("neo4j","XQKv5wEiB4QnaZG")
def timed(fn): t=time.time(); r=fn(); return r, round(time.time()-t,4)

# Part 2.1 — Q1: Stations reachable by a given user through their trips
def q1(user_id=1):
    with GraphDatabase.driver(URI, auth=AUTH) as drv, drv.session() as s:
        res = s.run("""
            MATCH (u:USER {id:$uid})-[:PERFORMED]->(t:TRIP)-[:STARTS_AT|ENDS_AT]->(st:STATION)
            RETURN DISTINCT st.id AS id, st.name AS name, st.city AS city
            ORDER BY st.name
        """, uid=user_id)
        return [dict(r) for r in res]

# Part 2.1 — Q2: Top 3 most important stations by total trips (incoming + outgoing)
def q2():
    with GraphDatabase.driver(URI, auth=AUTH) as drv, drv.session() as s:
        res = s.run("""
            MATCH (t:TRIP)-[:STARTS_AT|ENDS_AT]->(st:STATION)
            WITH st, count(t) AS total
            ORDER BY total DESC LIMIT 3
            RETURN st.id AS id, st.name AS name, total AS total_trips
        """)
        return [dict(r) for r in res]

if __name__ == "__main__":
    res1, t1 = timed(lambda: q1(1))
    print(f"Q1 (user_id=1 reachable stations): {len(res1)} in {t1}s")
    for r in res1[:5]: print(" ", r)

    res2, t2 = timed(q2)
    print(f"\nQ2 (top 3 stations): {t2}s")
    for r in res2: print(" ", r)