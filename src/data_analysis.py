import sqlite3
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_and_store_stats(cursor):
    """
    Calculate weather statistics for each station and year, and store the results in the weather_stats table.

    Args:
        cursor: An SQLite cursor object to use for executing database queries.
    """
    # Execute a SQL query to calculate weather statistics
    cursor.execute("""
        INSERT OR REPLACE INTO weather_stats (station_id, year, avg_max_temperature, avg_min_temperature, total_precipitation)
        SELECT
            station_id,
            strftime('%Y', date) AS year,
            AVG(CASE WHEN w.max_temperature != -9999 THEN max_temperature * 0.1 END) AS avg_max_temperature,
            AVG(CASE WHEN w.min_temperature != -9999 THEN min_temperature * 0.1 END) AS avg_min_temperature,
            SUM(CASE WHEN w.precipitation != -9999 THEN precipitation * 0.1 END) AS total_precipitation
        FROM weather_data w 
        JOIN weather_stations s
        ON s.id = w.station_id
        GROUP BY station_id, year
    """)

    # Log the number of rows affected by the SQL query
    logger.info(f"{cursor.rowcount} rows affected")

def main():
    """
    Entry point of the script.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Calculate weather statistics.")
    parser.add_argument("--db_path", type=str, required=True, help="The path to the SQLite database file.")
    args = parser.parse_args()

    # Connect to the database
    conn = sqlite3.connect(args.db_path)
    cursor = conn.cursor()

    # Calculate and store weather statistics
    calculate_and_store_stats(cursor)

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
