# part1/queries_mongodb.py — Part 1.2: MongoDB Queries (Q1–Q4)
from pymongo import MongoClient
import time

db = MongoClient()["adm_db"]
def timed(fn): t=time.time(); r=fn(); return r, round(time.time()-t,4)

# Part 1.2 — Q1: All trips with user info and station names ($lookup = JOIN)
def q1():
    return list(db.trips.aggregate([
        {"$lookup":{"from":"users",    "localField":"user_id",          "foreignField":"id","as":"user"}},
        {"$lookup":{"from":"stations", "localField":"start_station_id", "foreignField":"id","as":"s_st"}},
        {"$lookup":{"from":"stations", "localField":"end_station_id",   "foreignField":"id","as":"e_st"}},
        {"$unwind":"$user"}, {"$unwind":"$s_st"}, {"$unwind":"$e_st"},
        {"$project":{"_id":0,"id":1,"user.name":1,"user.surname":1,
                     "start_station":"$s_st.name","end_station":"$e_st.name",
                     "start_time":1,"end_time":1,"cost":1}}
    ]))

# Part 1.2 — Q2: All users with trip count and avg duration
def q2():
    agg = {r["_id"]: r for r in db.trips.aggregate([
        {"$addFields":{"dur":{"$subtract":[{"$toDate":"$end_time"},{"$toDate":"$start_time"}]}}},
        {"$group":{"_id":"$user_id","trip_count":{"$sum":1},"avg_ms":{"$avg":"$dur"}}}
    ])}
    result = []
    for u in db.users.find({},{"_id":0}):
        a = agg.get(u["id"], {})
        result.append({**u, "trip_count": a.get("trip_count",0),
                       "avg_duration_min": round(a.get("avg_ms",0)/60000, 2)})
    return result

# Part 1.2 — Q3: Stations with trip start/end counts
def q3():
    starts = {r["_id"]:r["c"] for r in db.trips.aggregate([{"$group":{"_id":"$start_station_id","c":{"$sum":1}}}])}
    ends   = {r["_id"]:r["c"] for r in db.trips.aggregate([{"$group":{"_id":"$end_station_id",  "c":{"$sum":1}}}])}
    return [{"id":s["id"],"name":s["name"],"city":s["city"],
             "trips_starting":starts.get(s["id"],0),"trips_ending":ends.get(s["id"],0)}
            for s in db.stations.find({},{"_id":0})]

# Part 1.2 — Q4: Trips with at least one ERROR event (fast: events are embedded)
def q4():
    return list(db.trips.find({"events.type":"ERROR"},
                               {"_id":0,"id":1,"user_id":1,"start_time":1,"end_time":1,"cost":1}))

if __name__ == "__main__":
    for name, fn in [("Q1",q1),("Q2",q2),("Q3",q3),("Q4",q4)]:
        res, t = timed(fn)
        print(f"MongoDB {name}: {len(res)} rows in {t}s")