import json
import pandas as pd
from geopy.distance import geodesic
from datetime import datetime
from sklearn.cluster import KMeans
import numpy as np

# Event data
#events = [
#    ('2025-01-04', 'Philadelphia', 'Band B'),
#    ('2025-01-06', 'Houston', 'Band G'),
#    ('2025-01-08', 'New York', 'Band A'),
#    ('2025-01-09', 'Los Angeles', 'Band F')
#]
bands=json.load(open('pollstar_sample_data.json'))
events = []
for event in bands['events']:
    print(event['band'])
    for tourDate in event['tourDates']:
        events.extend([(tourDate['date'],tourDate['location']['city'],event['band'])])
#for band, dates in bands['events'].items():
#    events.extend([(date, loc, band) for date, loc in dates])

# Sort by date

events.sort(key=lambda x: x[0])
print(events)
# Load city GPS coordinates
city_data_file = "cities.json"  # Replace with the actual file path
with open(city_data_file, "r") as f:
    city_data = json.load(f)

# Create a dictionary for quick city-to-coordinates mapping
city_coords = {entry["city"]: (entry["latitude"], entry["longitude"]) for entry in city_data}

# Merge events with GPS coordinates
def add_coordinates(events, city_coords):
    enriched_events = []
    for date, city, band in events:
        if city in city_coords:
            latitude, longitude = city_coords[city]
            enriched_events.append((date, city, band, latitude, longitude))
    return enriched_events

enriched_events = add_coordinates(events, city_coords)

# Convert to a DataFrame for processing
df = pd.DataFrame(enriched_events, columns=["Date", "City", "Band", "Latitude", "Longitude"])
df["Date"] = pd.to_datetime(df["Date"])

# Clustering Optimization Logic
def optimize_event_schedule(df, n_clusters=2):
    # Prepare data for clustering
    df["Date_ordinal"] = df["Date"].map(datetime.toordinal)
    clustering_data = df[["Latitude", "Longitude", "Date_ordinal"]].values

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["Cluster"] = kmeans.fit_predict(clustering_data)

    # Sort events within each cluster
    sorted_events = df.sort_values(by=["Cluster", "Date"]).reset_index(drop=True)
    return sorted_events

# Apply optimization
optimized_schedule = optimize_event_schedule(df, n_clusters=2)

# Display optimized schedule
print("Optimized Event Schedule:")
print(optimized_schedule[["Date", "City", "Band", "Cluster"]])
