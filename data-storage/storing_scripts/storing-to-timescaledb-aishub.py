import sys
import pandas as pd
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def storing(input_filename):
    # Đọc file dữ liệu thô
    print('storing ', input_filename)
    token = "l32Xnm-4VzOLAm7rdnGis6sywOyAUMyzCwlmsHu1vtG8kvX_eDbM1PEAiC78UTMguRGWHINdcWS6PyUXicKVdg=="
    INFLUXDB_ORG = "msf"
    INFLUXDB_BUCKET = "ais-data"

    client = InfluxDBClient(url="http://localhost:8086", token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    def write_chunk_to_influxdb(df_chunk):
        # convert timestamp string to timstamp unix
        df_chunk['Timestamp'] = pd.to_datetime(df_chunk['Timestamp'], format='%d/%m/%Y %H:%M:%S') 
        points = []
        for _, row in df_chunk.iterrows():
            point = Point("test1")
            for column in df_chunk.columns: 
                if row[column] and row[column] not in ['Unknown', 'Undefined']:
                    if column == "Timestamp":
                        point = point.time(row[column], write_precision='s')
                    elif column == 'IMO' and row[column]:
                        point = point.tag("IMO", row[column])
                    elif column == 'MMSI' and row[column]:
                        point = point.tag("MMSI", row[column])
                    else:
                        point = point.field(column, row[column])
            print(point)
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

# Take argument FILE_PATH from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage error: python script-number.py FILE_PATH")
    else:
        input_filename = sys.argv[1]
        storing(input_filename)
