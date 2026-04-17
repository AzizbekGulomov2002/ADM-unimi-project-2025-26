# part1/setup_postgres.py — Part 1.1: Relational Schema (PostgreSQL)
import psycopg2, csv

DB = {"dbname":"adm_db","user":"macbookairm2","password":"postgres","host":"localhost"}

def conn(): return psycopg2.connect(**DB)

def create_schema():
    # Part 1.1 — Relational schema: normalized, no embedding
    sql = """
    DROP TABLE IF EXISTS events, trips, stations, users CASCADE;

    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50), surname VARCHAR(50),
        birthdate DATE,  country VARCHAR(50)
    );
    CREATE TABLE stations (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100), city VARCHAR(50), capacity INTEGER
    );
    CREATE TABLE trips (
        id INTEGER PRIMARY KEY,
        user_id          INTEGER REFERENCES users(id),
        start_station_id INTEGER REFERENCES stations(id),
        end_station_id   INTEGER REFERENCES stations(id),
        start_time TIMESTAMP, end_time TIMESTAMP,
        cost DECIMAL(10,2)
    );
    CREATE TABLE events (
        id INTEGER PRIMARY KEY,
        trip_id   INTEGER REFERENCES trips(id),
        timestamp TIMESTAMP,
        type VARCHAR(10) CHECK (type IN ('GPS','ERROR','BATTERY','DELAY')),
        value TEXT
    );
    -- Part 1.2: indexes for faster queries
    CREATE INDEX idx_trips_user    ON trips(user_id);
    CREATE INDEX idx_trips_start   ON trips(start_station_id);
    CREATE INDEX idx_trips_end     ON trips(end_station_id);
    CREATE INDEX idx_events_trip   ON events(trip_id);
    CREATE INDEX idx_events_type   ON events(type);
    """
    with conn() as c:
        c.cursor().execute(sql); c.commit()
    print("PostgreSQL schema created.")

def load(table, path):
    with open(path) as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        rows = [tuple(r.values()) for r in reader]
    ph = ",".join(["%s"] * len(cols))
    with conn() as c:
        c.cursor().executemany(
            f"INSERT INTO {table} ({','.join(cols)}) VALUES ({ph}) ON CONFLICT DO NOTHING", rows)
        c.commit()
    print(f"  Loaded {len(rows)} → {table}")

if __name__ == "__main__":
    create_schema()
    load("users",    "data/users.csv")
    load("stations", "data/stations.csv")
    load("trips",    "data/trips.csv")
    load("events",   "data/events.csv")