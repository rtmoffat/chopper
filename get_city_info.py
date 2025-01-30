# %%
import json
import pandas as pd
from geonamescache import GeonamesCache
from io import StringIO
from geopy.distance import geodesic


# %% [markdown]
# # Load cities

# %%

city_file="cities500.json"
cities_df=pd.read_json(city_file)




# %% [markdown]
# # Grab only US and rename admin1 column to state

# %%
cities_df=cities_df[cities_df['country']=='US']
cities_df.rename(columns={'admin1':'state'},inplace=True)


# %% [markdown]
# # Get state abbreviations

# %%
gc=GeonamesCache()

states_df=pd.read_json(StringIO(json.dumps(gc.get_us_states())))
states_df=states_df.transpose()
states_df=states_df[['code','name']]
states_df.rename(columns={'code':'state_abbr','name':'state_name'},inplace=True)


# %% [markdown]
# # Add state abbreviations to original dataframe

# %%
cities_df=cities_df.merge(states_df,left_on='state',right_on='state_name')
cities_df.drop(columns=['state_name'])
cities_df.set_index('id')


# %% [markdown]
# # Caclulate distance between each city

# %%
between_two_cities=pd.DataFrame()
# Function to calculate distances

def calculate_distance(loc1, loc2):
    return geodesic(loc1, loc2).kilometers


# %% [markdown]
# # Cluster citiy distances into groups of a given kilometer range

# %%



