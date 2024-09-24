from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

class InfluxDBAdapter:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.query_api = self.client.query_api()
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def get_all_mmsi_numbers(self):
        """
        Fetch all unique MMSI numbers from the AIS data in the InfluxDB.
        """
        query = f'''
        from(bucket: "{self.bucket}")
        |> range(start: -30d)  // Adjust the range if needed
        |> filter(fn: (r) => r._measurement == "ais")
        |> keep(columns: ["mmsi"])
        |> distinct(column: "mmsi")
        '''
        try:
            result = self.query_api.query_data_frame(query)
            if not result.empty:
                return result['mmsi'].unique().tolist()
            else:
                return []
        except Exception as e:
            print(f"Error fetching MMSI numbers: {e}")
            return []

    def get_ship_data(self, mmsi: str, start_date: str, end_date: str):
        """
        Retrieve AIS data for a specific ship (MMSI) between two dates.
        
        :param mmsi: MMSI number of the ship (string).
        :param start_date: Start date for the query (ISO 8601 format).
        :param end_date: End date for the query (ISO 8601 format).
        :return: Pandas DataFrame with AIS data (lat, lon, timestamp).
        """
        query = f'''
        from(bucket: "{self.bucket}")
        |> range(start: {start_date}, stop: {end_date})
        |> filter(fn: (r) => r._measurement == "ais")
        |> filter(fn: (r) => r.mmsi == "{mmsi}")
        |> filter(fn: (r) => r._field == "lat" or r._field == "lon")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> keep(columns: ["_time", "lat", "lon", "mmsi"])
        '''
        try:
            result = self.query_api.query_data_frame(query)
            if not result.empty:
                return result[['mmsi', '_time', 'lat', 'lon']]
            else:
                return pd.DataFrame(columns=['mmsi', '_time', 'lat', 'lon'])
        except Exception as e:
            print(f"Error fetching ship data: {e}")
            return pd.DataFrame(columns=['mmsi', '_time', 'lat', 'lon'])

    def get_all_ships_data(self, start_date: str, end_date: str):
        """
        Retrieve AIS data for all ships between two dates.
        
        :param start_date: Start date for the query (ISO 8601 format).
        :param end_date: End date for the query (ISO 8601 format).
        :return: Pandas DataFrame with AIS data (mmsi, lat, lon, timestamp).
        """
        query = f'''
        from(bucket: "{self.bucket}")
        |> range(start: {start_date}, stop: {end_date})
        |> filter(fn: (r) => r._measurement == "ais")
        |> filter(fn: (r) => r._field == "lat" or r._field == "lon")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> keep(columns: ["_time", "lat", "lon", "mmsi"])
        '''
        try:
            result = self.query_api.query_data_frame(query)
            if not result.empty:
                return result[['mmsi', '_time', 'lat', 'lon']]
            else:
                return pd.DataFrame(columns=['mmsi', '_time', 'lat', 'lon'])
        except Exception as e:
            print(f"Error fetching data for all ships: {e}")
            return pd.DataFrame(columns=['mmsi', '_time', 'lat', 'lon'])

    def write_ais_data(self, mmsi: str, lat: float, lon: float, timestamp: str):
        """
        Write AIS data for a specific ship into the InfluxDB.
        
        :param mmsi: MMSI number of the ship (string).
        :param lat: Latitude of the ship (float).
        :param lon: Longitude of the ship (float).
        :param timestamp: Timestamp of the data point (ISO 8601 format).
        """
        point = {
            "measurement": "ais",
            "tags": {"mmsi": mmsi},
            "fields": {"lat": lat, "lon": lon},
            "time": timestamp
        }
        try:
            self.write_api.write(self.bucket, self.org, point)
            print(f"Successfully written data for MMSI: {mmsi}")
        except Exception as e:
            print(f"Error writing AIS data: {e}")

    def close(self):
        """
        Close the InfluxDB client connection.
        """
        self.client.close()

# Example Usage:
if __name__ == "__main__":
    # Initialize InfluxDB Adapter
    adapter = InfluxDBAdapter(
        url="http://localhost:8086",
        token="your_influxdb_token",
        org="your_org",
        bucket="ais_data_bucket"
    )

    # Get all MMSI numbers
    mmsi_numbers = adapter.get_all_mmsi_numbers()
    print("MMSI numbers:", mmsi_numbers)

    # Fetch data for a specific ship between two dates
    start_date = "2024-07-01T00:00:00Z"
    end_date = "2024-07-31T23:59:59Z"
    ship_data = adapter.get_ship_data("123456789", start_date, end_date)
    print("Ship data:", ship_data)

    # Fetch data for all ships between two dates
    all_ships_data = adapter.get_all_ships_data(start_date, end_date)
    print("All ships data:", all_ships_data)

    # Example of writing AIS data
    adapter.write_ais_data(mmsi="123456789", lat=52.5200, lon=13.4050, timestamp="2024-07-10T12:00:00Z")

    # Close the adapter when done
    adapter.close()
