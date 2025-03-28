import sys
import pandas as pd
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def storing(input_filename):
    # Đọc file dữ liệu thô
    print('clean in script-2.py')
    token = "l32Xnm-4VzOLAm7rdnGis6sywOyAUMyzCwlmsHu1vtG8kvX_eDbM1PEAiC78UTMguRGWHINdcWS6PyUXicKVdg=="
    INFLUXDB_ORG = "msf"
    INFLUXDB_BUCKET = "ais-data"

    client = InfluxDBClient(url="http://localhost:8086", token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    def write_chunk_to_influxdb(df_chunk):
        # convert timestamp string to timstamp unix
        df_chunk['timestamp'] = pd.to_datetime(df_chunk['timestamp'], format='%Y-%m-%d %H:%M:%S') 
        points = []
        for _, row in df_chunk.iterrows():
            point = Point("test1")
            for column in df_chunk.columns: 
                if row[column] and row[column] not in ['Unknown', 'Undefined']:
                    if column == "timestamp":
                        point = point.time(row[column], write_precision='s')
                    elif column == 'imo' and row[column]:
                        point = point.tag("imo", row[column])
                    elif column == 'mmsi' and row[column]:
                        point = point.tag("mmsi", row[column])
                    else:
                        point = point.field(column, row[column])
            points.append(point)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)
        print(f"Written {len(points)} points to InfluxDB")

    chunk_size = 10000  # Kích thước mỗi chunk, bạn có thể điều chỉnh kích thước này
    i = 1
    for chunk in pd.read_csv(input_filename, chunksize=chunk_size):
        write_chunk_to_influxdb(chunk)
        print(f"Data loaded successfully into InfluxDB. Chunk #{i}")
        i += 1
        break

# Lấy argument FILE_PATH từ command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage error: python script-number.py FILE_PATH")
    else:
        input_filename = sys.argv[1]
        storing(input_filename)
