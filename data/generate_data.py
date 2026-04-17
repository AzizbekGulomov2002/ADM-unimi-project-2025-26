# generate_data.py — generates CSV test data for all benchmark configs
import csv, random, os
from datetime import datetime, timedelta

NAMES    = ["Alice","Bob","Carlo","Diana","Eva","Luca","Marco","Sofia"]
SURNAMES = ["Rossi","Bianchi","Ferrari","Esposito","Romano","Ricci"]
COUNTRIES= ["Italy","Germany","France","Spain","USA","UK"]
CITIES   = ["Milan","Rome","Turin","Naples","Florence","Venice"]
ETYPES   = ["GPS","ERROR","BATTERY","DELAY"]

def gen(n_users=1000, n_trips=10000, n_events=2, n_stations=50, out="data"):
    os.makedirs(out, exist_ok=True)
    rng  = random.Random(42)
    base = datetime(2024, 1, 1)

    users    = [[i, rng.choice(NAMES), rng.choice(SURNAMES),
                 f"19{rng.randint(60,99)}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}",
                 rng.choice(COUNTRIES)] for i in range(1, n_users+1)]

    stations = [[i, f"Station_{i}", rng.choice(CITIES), rng.randint(10,50)]
                for i in range(1, n_stations+1)]

    trips, events, eid = [], [], 1
    for i in range(1, n_trips+1):
        st = base + timedelta(minutes=rng.randint(0, 525600))
        en = st + timedelta(minutes=rng.randint(5, 120))
        trips.append([i, rng.randint(1, n_users), rng.randint(1, n_stations),
                      rng.randint(1, n_stations), st, en, round(rng.uniform(1,30), 2)])
        for _ in range(n_events):
            events.append([eid, i, st + timedelta(minutes=rng.randint(1,30)),
                           rng.choice(ETYPES), round(rng.uniform(0,100), 1)])
            eid += 1

    _csv(f"{out}/users.csv",    ["id","name","surname","birthdate","country"], users)
    _csv(f"{out}/stations.csv", ["id","name","city","capacity"], stations)
    _csv(f"{out}/trips.csv",    ["id","user_id","start_station_id","end_station_id",
                                  "start_time","end_time","cost"], trips)
    _csv(f"{out}/events.csv",   ["id","trip_id","timestamp","type","value"], events)
    print(f"Generated: {n_users} users | {n_stations} stations | {n_trips} trips | {len(events)} events")

def _csv(path, hdr, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(hdr); w.writerows(rows)

if __name__ == "__main__":
    gen()   # default: 1k users, 10k trips, 2 events/trip