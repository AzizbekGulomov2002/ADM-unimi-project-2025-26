# part1/queries_postgres.py — Part 1.2: PostgreSQL Queries (Q1–Q4)
import psycopg2, time

DB = {"dbname":"adm_db","user":"macbookairm2","password":"postgres","host":"localhost"}
def conn(): return psycopg2.connect(**DB)
def timed(fn): t=time.time(); r=fn(); return r, round(time.time()-t,4)

# Part 1.2 — Q1: All trips with user info and station names
def q1():
    with conn() as c:
        cur = c.cursor()
        cur.execute("""
            SELECT t.id, u.name, u.surname, u.country,
                   s1.name AS start_station, s2.name AS end_station,
                   t.start_time, t.end_time, t.cost
            FROM trips t
            JOIN users    u  ON t.user_id          = u.id
            JOIN stations s1 ON t.start_station_id = s1.id
            JOIN stations s2 ON t.end_station_id   = s2.id
        """)
        return cur.fetchall()

# Part 1.2 — Q2: All users with trip count and average duration (minutes)
def q2():
    with conn() as c:
        cur = c.cursor()
        cur.execute("""
            SELECT u.id, u.name, u.surname,
                   COUNT(t.id) AS trip_count,
                   COALESCE(AVG(EXTRACT(EPOCH FROM (t.end_time - t.start_time))/60), 0) AS avg_min
            FROM users u
            LEFT JOIN trips t ON u.id = t.user_id
            GROUP BY u.id, u.name, u.surname
        """)
        return cur.fetchall()

# Part 1.2 — Q3: All stations with number of trips starting/ending there
def q3():
    with conn() as c:
        cur = c.cursor()
        cur.execute("""
            SELECT s.id, s.name, s.city,
                   COUNT(t1.id) AS trips_starting,
                   COUNT(t2.id) AS trips_ending
            FROM stations s
            LEFT JOIN trips t1 ON s.id = t1.start_station_id
            LEFT JOIN trips t2 ON s.id = t2.end_station_id
            GROUP BY s.id, s.name, s.city
        """)
        return cur.fetchall()

# Part 1.2 — Q4: Trips that have at least one ERROR event
def q4():
    with conn() as c:
        cur = c.cursor()
        cur.execute("""
            SELECT DISTINCT t.id, t.user_id, t.start_time, t.end_time, t.cost
            FROM trips t
            JOIN events e ON t.id = e.trip_id
            WHERE e.type = 'ERROR'
        """)
        return cur.fetchall()

if __name__ == "__main__":
    for name, fn in [("Q1",q1),("Q2",q2),("Q3",q3),("Q4",q4)]:
        res, t = timed(fn)
        print(f"PostgreSQL {name}: {len(res)} rows in {t}s")