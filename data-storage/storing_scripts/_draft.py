import sys
import pandas as pd
import os
import psycopg2

def write_chunk_to_db(cursor, conn, df_chunk):
    insert_query = """INSERT INTO ais_data (timestamp, imo, mmsi, data) VALUES (%s, %s, %s, %s)"""
    
    # convert timestamp string to timstamp unix
    df_chunk['Timestamp'] = pd.to_datetime(df_chunk['Timestamp'], format='%d/%m/%Y %H:%M:%S') 
    
    for _, row in df_chunk.iterrows():
        (timestamp, imo, mmsi, data) = (None, None, None, None)
        for column in df_chunk.columns: 
            if column == "Timestamp":
                timestamp = row['Timestamp']
            elif column == "IMO":
                imo = row['imo']
            elif column == "MMSI":
                mmsi = row['mmsi']
            else:
                data = row[column]
        cursor.execute(insert_query, (timestamp, imo, mmsi, data))
    conn.commit()

def storing(input_filename):
    # Đọc file dữ liệu thô
    print('storing ', input_filename)
    
    #CONNECTION = "postgres://username:password@host:port/dbname"
    CONNECTION = "dbname=ovd user=admin password=admin host=localhost port=5432"
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()

    chunk_size = 10000  # Kích thước mỗi chunk, bạn có thể điều chỉnh kích thước này
    i = 1
    for chunk in pd.read_csv(input_filename, chunksize=chunk_size):
        write_chunk_to_db(cursor, conn, chunk)
        print(f"Data loaded successfully into TimescaleDB. Chunk #{i}")
        i += 1

# Take argument FILE_PATH from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage error: python script-number.py FILE_PATH")
    else:
        input_filename = sys.argv[1]
        storing(input_filename)
