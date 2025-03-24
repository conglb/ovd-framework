from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

#########
# Purpose
#########
# historical data from dmk.dk
# this is data ingestion
# Thông tin kết nối
token = "l32Xnm-4VzOLAm7rdnGis6sywOyAUMyzCwlmsHu1vtG8kvX_eDbM1PEAiC78UTMguRGWHINdcWS6PyUXicKVdg=="
INFLUXDB_ORG = "msf"
INFLUXDB_BUCKET = "ais-data"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Prepare the data
# Đường dẫn tệp CSV
CSV_FILE_PATH = "/data/raw_files/aishub.com/aishub-2025-01-12_12.37.12.csv"

def write_chunk_to_influxdb(df_chunk):
    # Structure #
    # measurement: "DKA.mk"
    # tags: 
    #   imo,
    #   mmsi, 
    #   vessel_name 
    # fields:
    #         
    # timestamp 

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
for chunk in pd.read_csv(CSV_FILE_PATH, chunksize=chunk_size):
    write_chunk_to_influxdb(chunk)
    print(f"Data loaded successfully into InfluxDB. Chunk #{i}")
    i += 1
    break




'''
query_api = client.query_api()

query = """from(bucket: "ais-data")
 |> range(start: -10y)
 |> filter(fn: (r) => r._measurement == "ais-data")"""
tables = query_api.query(query, org="msf")
print(tables)
for table in tables:
  for record in table.records:
    print(record)
'''