import sys
import pandas as pd
import os
import psycopg2
import json
import time
from psycopg2.extras import execute_values

def log_performance(file_size, time_spent):
    with open('./performance_log.log', 'a') as f:
        f.write(f"{file_size},{time_spent}\n")

# take 6s to run 55MB file
def write_chunk_to_db(cursor, conn, df_chunk):
    insert_query = """
    INSERT INTO ais_data (
        timestamp, mmsi, imo, ship_type, heading, course, speed, navstatus, 
        name, callsign, draught, destination, eta, latitude, longitude, extra
    ) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Prepare a list of tuples for batch insertion
    records = []
    
    for _, row in df_chunk.iterrows():
        extra = {
            'type': 0 if pd.isna(row.get('type')) else row.get('type'),
            'A': -1 if pd.isna(row.get('type')) else row.get('type'),
            'B': -1 if pd.isna(row.get('type')) else row.get('type'),
            'C': -1 if pd.isna(row.get('type')) else row.get('type'),
            'D': -1 if pd.isna(row.get('type')) else row.get('type')
        }

        record = (
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
            #row.get('eta'),  # Uncommented ETA field
            None,
            row.get('latitude'),
            row.get('longitude'),
            json.dumps(extra)
        )
        records.append(record)

    # Batch insert all rows at once
    cursor.executemany(insert_query, records)
    conn.commit()

# take 3s to run 55MB file
def write_chunk_to_db_optimized(cursor, conn, df_chunk):
    # Prepare insert query
    insert_query = """
    INSERT INTO ais_data (
        timestamp, mmsi, imo, ship_type, heading, course, speed, navstatus, 
        name, callsign, draught, destination, eta, latitude, longitude, extra
    ) VALUES %s
    """

    # Build the data for insertion
    records = [
        (
            row.get('# Timestamp'),
            row.get('MMSI'),
            row.get('IMO'),
            row.get('Ship type'),
            row.get('Heading'),
            row.get('COG'),
            row.get('SOG'),
            row.get('Navigational status'),
            row.get('Name'),
            row.get('Callsign'),
            row.get('Draught'),
            row.get('Destination'),
            None,  # Uncommented ETA
            row.get('Latitude'),
            row.get('Longitude'),
            json.dumps({
                'type': 0 if pd.isna(row.get('Type of mobile')) else row.get('Type of mobile'),
                'A': -1 if pd.isna(row.get('A')) else row.get('A'),
                'B': -1 if pd.isna(row.get('B')) else row.get('B'),
                'C': -1 if pd.isna(row.get('C')) else row.get('C'),
                'D': -1 if pd.isna(row.get('D')) else row.get('D')
            })
        )
        for _, row in df_chunk.iterrows()
    ]

    # Execute a highly optimized bulk insert using execute_values
    execute_values(cursor, insert_query, records)
    conn.commit()


def storing(input_filepath):
    # Đọc file dữ liệu thô
    print('storing ', input_filepath)
    
    conn = psycopg2.connect(
            dbname="ovd",
            user="admin",
            password="admin",
            host="timescaledb_ovd",
            port="5432"
        )
    cursor = conn.cursor()

    chunk_size = 10000  # Kích thước mỗi chunk, bạn có thể điều chỉnh kích thước này
    i = 1
    for chunk in pd.read_csv(input_filepath, chunksize=chunk_size):
        write_chunk_to_db_optimized(cursor, conn, chunk)
        print(f"Data loaded successfully into TimescaleDB. Chunk #{i}")
        i += 1

# Take argument FILE_PATH from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage error: python script-number.py FILE_PATH")
    else:
        input_filepath = sys.argv[1]
        time_start = time.time()
        storing(input_filepath)
        time_end = time.time()
        print('log')
        log_performance(os.path.getsize(input_filepath), time_end - time_start)
