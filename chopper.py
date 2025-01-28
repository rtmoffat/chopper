import numpy as np
import pandas as pd
from geopy.distance import geodesic
from itertools import permutations
import json

# Sample input
#bands = {
#    "Band A": [("2025-03-10", "New York"), ("2025-03-15", "Boston")],
#    "Band B": [("2025-03-12", "Philadelphia"), ("2025-03-20", "New York")],
#    "Band C": [("2025-03-18", "Boston"), ("2025-03-25", "Washington D.C.")],
#}
bands=json.load(open('pollstar_sample_data.json'))

#locations = {
#    "New York": (40.7128, -74.0060),
#    "Boston": (42.3601, -71.0589),
#    "Philadelphia": (39.9526, -75.1652),
#    "Washington D.C.": (38.9072, -77.0369),
#}
#locations=json.load(open('cities.json'))
locations=pd.read_json('cities.json')
# Function to calculate distances
def calculate_distance(loc1, loc2):
    return geodesic(loc1, loc2).kilometers

# Function to optimize
def find_optimal_itinerary(bands):
    all_dates = []
    for event in bands['events']:
        print(event['band'])
        for tourDate in event['tourDates']:
            all_dates.extend([(tourDate['date'],tourDate['location']['city'],event['band'])])
    #for band, dates in bands['events'].items():
    #    all_dates.extend([(date, loc, band) for date, loc in dates])

    # Sort by date
    
    all_dates.sort(key=lambda x: x[0])
    print(all_dates)
    best_itinerary = None
    min_distance = float('inf')

    # Check all permutations of dates
    print(len(all_dates))
    perms=permutations(all_dates)
    for perm in perms:
        print(len(perm))
        current_distance = 0
        for i in range(len(perm) - 1):
            #loc1[i]=(locations[perm[i][1]])
            #x=locations[locations['city']=='Pittsburgh']['latitude'].to_list()[0]
            loc={}
            loc['lat']=locations[locations['city'] == perm[i][1]]['latitude'].to_list()[0]
            loc['lon']=locations[locations['city'] == perm[i][1]]['longitude'].to_list()[0]
            loc1 = (loc['lat'],loc['lon'])
            loc['lat']=locations[locations['city'] == perm[i+1][1]]['latitude'].to_list()[0]
            loc['lon']=locations[locations['city'] == perm[i+1][1]]['longitude'].to_list()[0]
            loc2 = (loc['lat'],loc['lon'])
            current_distance += calculate_distance(loc1, loc2)

        # Update best itinerary
        if current_distance < min_distance:
            min_distance = current_distance
            best_itinerary = perm

    return best_itinerary, min_distance

# Run the algorithm
itinerary, distance = find_optimal_itinerary(bands)

# Print result
print("Optimal Itinerary:")
for date, loc, band in itinerary:
    print(f"{band} - {loc} on {date}")
print(f"Total Distance: {distance:.2f} km")
