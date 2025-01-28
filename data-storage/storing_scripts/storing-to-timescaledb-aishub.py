import sys
import pandas as pd
import os
import psycopg2
import json
import time

def log_performance(file_size, time_spent):
    with open('./performance_log.log', 'a') as f:
        f.write(f"{file_size},{time_spent}\n")

def write_chunk_to_db(cursor, conn, df_chunk):
    insert_query = """INSERT INTO ais_data (timestamp, mmsi, imo, ship_type, heading, course, speed, navstatus, name, callsign, draught, destination, eta, latitude, longitude, extra) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    # convert timestamp string to timstamp unix
    #df_chunk['timestamp'] = pd.to_datetime(df_chunk['timestamp'], format='%d/%m/%Y %H:%M:%S') 
    
    for _, row in df_chunk.iterrows():
        (timestamp, mmsi, imo, ship_type, heading, course, speed, navstatus, name, callsign, draught, destination, eta, latitude, longitude, extra) = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  {})
        
        timestamp = row.get('timestamp')
        mmsi = row.get('mmsi')
        imo = row.get('imo')
        ship_type = row.get('ship_type')
        heading = row.get('heading')
        course = row.get('course')
        speed = row.get('speed')
        navstatus = row.get('navstatus')
        name = row.get('name')
        callsign = row.get('callsign')
        draught = row.get('draught')
        destination = row.get('destination')
        #eta = row.get('eta')
        latitude = row.get('latitude')
        longitude = row.get('longitude')
        extra['type'] = 0 if pd.isna(row['type']) else row['type']
        extra['A'] = -1 if pd.isna(row['type']) else row['type']
        extra['B'] = -1 if pd.isna(row['type']) else row['type']
        extra['C'] = -1 if pd.isna(row['type']) else row['type']
        extra['D'] = -1 if pd.isna(row['type']) else row['type']
        
        cursor.execute(insert_query, (timestamp, mmsi, imo, ship_type, heading, course, speed, navstatus, name, callsign, draught, destination, eta, latitude, longitude, json.dumps(extra)) )
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
        write_chunk_to_db(cursor, conn, chunk)
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
