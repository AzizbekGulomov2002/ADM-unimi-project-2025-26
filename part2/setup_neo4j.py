# part2/setup_neo4j.py — Part 2.1: Neo4j Graph Schema
# Nodes: USER, STATION, TRIP  |  Edges: PERFORMED, STARTS_AT, ENDS_AT
from neo4j import GraphDatabase
import csv

URI  = "bolt://localhost:7687"
AUTH = ("neo4j", "XQKv5wEiB4QnaZG")

def load_all():
    with GraphDatabase.driver(URI, auth=AUTH) as drv, drv.session() as s:
        s.run("MATCH (n) DETACH DELETE n")  # clear

        # Part 2.1 — USER nodes
        with open("data/users.csv") as f: users = list(csv.DictReader(f))
        s.run("UNWIND $r AS r MERGE (u:USER {id:toInteger(r.id)}) SET u.name=r.name, u.surname=r.surname, u.country=r.country", r=users)

        # Part 2.1 — STATION nodes
        with open("data/stations.csv") as f: stas = list(csv.DictReader(f))
        s.run("UNWIND $r AS r MERGE (s:STATION {id:toInteger(r.id)}) SET s.name=r.name, s.city=r.city", r=stas)

        # Part 2.1 — TRIP nodes
        with open("data/trips.csv") as f: trips = list(csv.DictReader(f))
        s.run("UNWIND $r AS r MERGE (t:TRIP {id:toInteger(r.id)}) SET t.cost=toFloat(r.cost)", r=trips)

        # Part 2.1 — PERFORMED edges (USER → TRIP)
        s.run("UNWIND $r AS r MATCH (u:USER {id:toInteger(r.user_id)}),(t:TRIP {id:toInteger(r.id)}) MERGE (u)-[:PERFORMED]->(t)", r=trips)

        # Part 2.1 — STARTS_AT edges (TRIP → STATION)
        s.run("UNWIND $r AS r MATCH (t:TRIP {id:toInteger(r.id)}),(s:STATION {id:toInteger(r.start_station_id)}) MERGE (t)-[:STARTS_AT]->(s)", r=trips)

        # Part 2.1 — ENDS_AT edges (TRIP → STATION)
        s.run("UNWIND $r AS r MATCH (t:TRIP {id:toInteger(r.id)}),(s:STATION {id:toInteger(r.end_station_id)}) MERGE (t)-[:ENDS_AT]->(s)", r=trips)

        print(f"Neo4j loaded: {s.run('MATCH (u:USER) RETURN count(u) AS c').single()['c']} users | "
              f"{s.run('MATCH (s:STATION) RETURN count(s) AS c').single()['c']} stations | "
              f"{s.run('MATCH (t:TRIP) RETURN count(t) AS c').single()['c']} trips")

if __name__ == "__main__":
    load_all()