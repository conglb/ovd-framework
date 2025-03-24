import sys
import pandas as pd
import os

CLEANED_FILES_DIR = "../data/cleaned_files"

def clean(input_filename, output_filename):
    """
    Args:
        input_filename (string): path to the file will be cleaned

    Returns:
        DataFrame: path to the cleaned file
    """
    # Đọc file dữ liệu thô
    print('clean in s2.py')
    df = pd.read_csv(input_filename)
    df = df.rename(columns={"MMSI":'mmsi','TSTAMP': 'timestamp', 'LATITUDE':'latitude', 'LONGITUDE':'longitude','COG':'cog','SOG':'sog','HEADING':'heading','NAVSTAT':'navstat','IMO':'imo','NAME':'name','CALLSIGN':'callsign','DRAUGHT':'draught','DEST':'dest','ETA':'eta',"TYPE":'type'})
    df.dropna(subset=['mmsi', 'timestamp', 'latitude', 'longitude'], how='any', inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"].str.replace("GMT", "").str.strip(), format="%Y-%m-%d %H:%M:%S")

    df['eta'] = pd.to_datetime(df["eta"], format="%m-%d %H:%M", errors='coerce')
    df['eta'] = df['eta'].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

    df = df.sort_values(by='timestamp', ascending=True)
    df = df.reset_index(drop=True)

    df['imo'].replace(0, pd.NA, inplace=True)

    # Lưu DataFrame đã làm sạch vào CSV
    df.to_csv(output_filename, index=False)
    return output_filename

# Lấy argument FILE_PATH từ command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_script1.py FILE_PATH OUTPUT_PATH")
    else:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        print(f'cleaned file is: {clean(input_filename, output_filename)}')
