# part1/setup_mongodb.py — Part 1.1: Document Schema (MongoDB)
# Design choice: events EMBEDDED inside trips (avoids joins for Q4)
# users and stations kept as separate collections (referenced by id)
import csv
from pymongo import MongoClient

db = MongoClient()["adm_db"]

def load_all():
    # Part 1.1 — Drop and reload
    db.users.drop(); db.stations.drop(); db.trips.drop()

    with open("data/users.csv") as f:
        users = [{"id":int(r["id"]),"name":r["name"],"surname":r["surname"],
                  "birthdate":r["birthdate"],"country":r["country"]}
                 for r in csv.DictReader(f)]
    db.users.insert_many(users)

    with open("data/stations.csv") as f:
        stations = [{"id":int(r["id"]),"name":r["name"],
                     "city":r["city"],"capacity":int(r["capacity"])}
                    for r in csv.DictReader(f)]
    db.stations.insert_many(stations)

    # Group events by trip_id first (for embedding)
    evts = {}
    with open("data/events.csv") as f:
        for r in csv.DictReader(f):
            evts.setdefault(int(r["trip_id"]), []).append(
                {"type":r["type"],"timestamp":r["timestamp"],"value":r["value"]})

    with open("data/trips.csv") as f:
        trips = [{"id":int(r["id"]),"user_id":int(r["user_id"]),
                  "start_station_id":int(r["start_station_id"]),
                  "end_station_id":int(r["end_station_id"]),
                  "start_time":r["start_time"],"end_time":r["end_time"],
                  "cost":float(r["cost"]),
                  "events": evts.get(int(r["id"]), [])}   # ← embedded events
                 for r in csv.DictReader(f)]
    db.trips.insert_many(trips)

    # Part 1.2: indexes
    db.trips.create_index("user_id")
    db.trips.create_index("start_station_id")
    db.trips.create_index("end_station_id")
    db.trips.create_index("events.type")
    print(f"MongoDB loaded: {db.users.count_documents({})} users | "
          f"{db.stations.count_documents({})} stations | {db.trips.count_documents({})} trips")

if __name__ == "__main__":
    load_all()