import sys
import pandas as pd
import os

def clean(input_file_path, output_file_path):
    # Read raw data
    df = pd.read_csv(input_file_path)

    # Start cleaning the data
    df_cleaned = df.dropna()         
    df_cleaned = df_cleaned.drop_duplicates()  

    # Return cleaned data to 
    df_cleaned.to_csv(output_file_path, index=False)
    return output_file_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py FILE_PATH OUTPUT_PATH")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        clean(input_file_path, output_file_path)