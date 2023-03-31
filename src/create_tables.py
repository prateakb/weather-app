import sqlite3
import argparse
import logging

logger = logging.getLogger(__name__)

def create_tables(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_stations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state VARCHAR(2) NOT NULL,
                station_code VARCHAR(10) NOT NULL UNIQUE
            );
        """)

        logger.info("weather_stations Table created successfully")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                station_id INTEGER,
                date DATE NOT NULL,
                max_temperature INTEGER NOT NULL,
                min_temperature INTEGER NOT NULL,
                precipitation INTEGER NOT NULL,
                FOREIGN KEY (station_id) REFERENCES weather_stations(id)
            );
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_weather_data_date ON weather_data(date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_weather_data_station_id ON weather_data(station_id);")
        
        logger.info("weather_data Table created successfully")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                station_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                avg_max_temperature REAL,
                avg_min_temperature REAL,
                total_precipitation REAL,
                FOREIGN KEY (station_id) REFERENCES weather_stations(id),
                UNIQUE (station_id, year)
            );
        """)
        logger.info("weather_stats Table created successfully")

        conn.commit()
        logger.info("Tables created successfully")

    except sqlite3.Error as e:
        logger.error(f"Error creating tables: {e}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create database tables.")
    parser.add_argument("--db_path", type=str, required=True, help="The path to the SQLite database file.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    create_tables(args.db_path)
