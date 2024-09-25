import os
import json

DATA_SOURCES_FILE = 'data_sources.json'

# Load data sources from JSON file
def load_data_sources():
    if os.path.exists(DATA_SOURCES_FILE):
        with open(DATA_SOURCES_FILE, 'r') as f:
            return json.load(f)
    return []

# Save data sources to JSON file
def save_data_sources(data_sources):
    with open(DATA_SOURCES_FILE, 'w') as f:
        json.dump(data_sources, f, indent=4)

# Add a new data source
def add_data_source(name, url, description):
    data_sources = load_data_sources()
    data_sources.append({
        "name": name,
        "url": url,
        "description": description
    })
    save_data_sources(data_sources)

# Delete a data source
def delete_data_source(index):
    data_sources = load_data_sources()
    if 0 <= index < len(data_sources):
        del data_sources[index]
    save_data_sources(data_sources)

# Edit a data source
def edit_data_source(index, name, url, description):
    data_sources = load_data_sources()
    if 0 <= index < len(data_sources):
        data_sources[index] = {
            "name": name,
            "url": url,
            "description": description
        }
    save_data_sources(data_sources)
