import pandas as pd
import json

# Load the data
cities = pd.read_json('cities500_us.json')
tourdates=pd.read_json('pollstar_condensed.json')
for city_state in tourdates['city']:
    print(city_state)
    city = city_state.split(',')[0].strip()
    state = city_state.split(',')[1].strip()
    cities = cities[cities['name'] != city]

    print(city)
    print(state)
