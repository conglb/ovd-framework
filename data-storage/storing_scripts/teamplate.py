import sys
import pandas as pd
import os
import psycopg2
import json
import time
from psycopg2.extras import execute_values


def write_chunk_to_db_optimized(cursor, conn, df_chunk):
    insert_query = """
    INSERT INTO ais_data (
        timestamp, mmsi, imo, ship_type, heading, course, speed, navstatus, 
        name, callsign, draught, destination, eta, latitude, longitude, extra
    ) VALUES %s
    """

    records = [
        (
            row.get('timestamp'),
            row.get('mmsi'),
            row.get('imo'),
            row.get('ship_type'),
            row.get('heading'),
            row.get('course'),
            row.get('speed'),
            row.get('navstatus'),
            row.get('name'),
            row.get('callsign'),
            row.get('draught'),
            row.get('destination'),
            None,  # Uncommented ETA
            row.get('latitude'),
            row.get('longitude'),
            json.dumps({
                'type': 0 if pd.isna(row.get('type')) else row.get('type'),
                'A': -1 if pd.isna(row.get('type')) else row.get('type'),
                'B': -1 if pd.isna(row.get('type')) else row.get('type'),
                'C': -1 if pd.isna(row.get('type')) else row.get('type'),
                'D': -1 if pd.isna(row.get('type')) else row.get('type')
            })
        )
        for _, row in df_chunk.iterrows()
    ]

    # Execute a optimized bulk insert using execute_values
    execute_values(cursor, insert_query, records)
    conn.commit()


def storing(input_filepath):
    
    conn = psycopg2.connect(
            dbname="ovd",
            user="admin",
            password="admin",
            host="timescaledb_ovd",
            port="5432"
        )
    cursor = conn.cursor()

    chunk_size = 10000 
    for chunk in pd.read_csv(input_filepath, chunksize=chunk_size):
        write_chunk_to_db_optimized(cursor, conn, chunk)

# Take argument FILE_PATH from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py FILE_PATH")
    else:
        input_file_path = sys.argv[1]
        storing(input_file_path)
