import os
import sqlite3
from datetime import datetime
import logging
import argparse
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATES = ["NE", "IA", "IL", "IN", "OH"]

def parse_weather_data_line(line):
    """
    Parse a line of weather data into its components.

    Args:
        line (str): A line of weather data.

    Returns:
        tuple: A tuple containing date, max_temperature, min_temperature, and precipitation.
    """
    date_str, max_temp, min_temp, precipitation = line.strip().split('\t')
    date = datetime.strptime(date_str, '%Y%m%d').date()
    return date, int(max_temp), int(min_temp), int(precipitation)

def process_weather_file(file_path, cursor):
    """
    Process a weather data file and ingest its contents into the database.

    Args:
        file_path: The path to the weather data file to process.
        cursor: An SQLite cursor object to use for executing database queries.

    Returns:
        The number of weather records ingested into the database.
    """
    records_ingested = 0
    start_time = datetime.now()
    logger.info(f"Starting ingesting {file_path} at {start_time}")

    # Choose a random state for the weather station
    station_code = random.choice(STATES)

    # Insert the station into the database if it doesn't already exist
    cursor.execute("""
        INSERT OR IGNORE INTO weather_stations (state, station_code) VALUES (?, ?)
    """, (station_code, station_code))

    # Retrieve the ID of the weather station from the database
    cursor.execute("""
        SELECT id FROM weather_stations WHERE station_code = ?
    """, (station_code,))
    station_id = cursor.fetchone()[0]

    # Parse each line in the weather data file and insert it into the database
    with open(file_path, 'r') as file:
        for line in file:
            try:
                date, max_temp, min_temp, precipitation = parse_weather_data_line(line)
                cursor.execute("""
                    INSERT OR IGNORE INTO weather_data (station_id, date, max_temperature, min_temperature, precipitation)
                    VALUES (?, ?, ?, ?, ?)
                """, (station_id, date, max_temp, min_temp, precipitation))
                if cursor.rowcount == 1:
                    records_ingested += 1
            except Exception as e:
                logger.error(f"Error processing line: {line.strip()} in {file_path}: {e}")

    end_time = datetime.now()
    logger.info(f"Finished ingesting {file_path} at {end_time}")
    logger.info(f"Time taken for {file_path}: {end_time - start_time}")

    return records_ingested


def ingest_weather_data(wx_data_directory, db_path):
    """
    Ingest weather data from the wx_data directory into the SQLite database.

    Args:
        wx_data_directory (str): The path to the wx_data directory.
        db_path (str): The path to the SQLite database file.
    """
    start_time = datetime.now()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    total_records_ingested = 0
    for root, _, files in os.walk(wx_data_directory):
        for file in files:
            file_path = os.path.join(root, file)
            records_ingested = process_weather_file(file_path, cursor)
            logger.info(f"{records_ingested} records ingested from {file_path}")
            total_records_ingested += records_ingested

    conn.commit()
    conn.close()

    end_time = datetime.now()
    logger.info(f"Started ingestion job at {start_time}")
    logger.info(f"Finished ingestion job at {end_time}")
    logger.info(f"Total time taken for whole job: {end_time - start_time}")
    logger.info(f"Total records ingested for whole job: {total_records_ingested}")

def main():
    parser = argparse.ArgumentParser(description="Ingest weather data into an SQLite database.")
    parser.add_argument("--wx_data_directory", type=str, required=True, help="The path to the wx_data directory.")
    parser.add_argument("--db_path", type=str, required=True, help="The path to the SQLite database file.")
    args = parser.parse_args()

    ingest_weather_data(args.wx_data_directory, args.db_path)

if __name__ == "__main__":
    main()
