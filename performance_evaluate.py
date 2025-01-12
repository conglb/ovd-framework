import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data from the provided string
data = """
File_size,Time
5689705,0.6221303939819336
5624033,0.4279520511627197
5602372,0.4748983383178711
5596288,0.8564126491546631
5599437,0.6171066761016846
"""

# Read the data into a DataFrame
from io import StringIO
df = pd.read_csv(StringIO(data))

# Scale the data
max_file_size = 1 * 1024**3  # 1GB in bytes
max_time = 10  # 10 seconds

df['Scaled_File_Size'] = df['File_size'] / max_file_size
df['Scaled_Time'] = df['Time'] / max_time

# Plot the scaled data
plt.figure(figsize=(8, 6))
plt.plot(df['Scaled_File_Size'], df['Scaled_Time'], marker='o', linestyle='-', color='b')
plt.xlabel('File Size (scaled to 1GB)', fontsize=12)
plt.ylabel('Time Taken (scaled to 10s)', fontsize=12)
plt.title('File Size vs Time Taken to Process (Scaled)', fontsize=14)
plt.grid(True)
plt.show()