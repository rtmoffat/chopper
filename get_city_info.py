# %%
import json
import pandas as pd
from geonamescache import GeonamesCache
from io import StringIO
from geopy.distance import geodesic
from threading import Thread
from queue import Queue
import concurrent.futures






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
cities_df=cities_df.merge(states_df,left_on='state',right_on='state_name',how='left')
cities_df.drop(columns=['state_name'])
cities_df.set_index('id')
cities_df.to_json('cities500_us.json',orient='records',indent=2)

# %% [markdown]
# # Caclulate distance between each city

# %%
def calculate_distance(loc1, loc2):
    return geodesic(loc1, loc2).kilometers

def distance_thread(q,index,cities_df):
    city1=cities_df.iloc[index]
    for j in range(index+1,len(cities_df)):
        city2=cities_df.iloc[j]
        distance=calculate_distance((city1['lat'],city1['lon']),(city2['lat'],city2['lon']))
        q.put({'city1':city1['name'],
                'city1_state':city1['state_abbr'],
                'city2':city2['name'],
                'city2_state':city2['state_abbr'],
                'distance':distance})
        if j%1000==0:
            print(j,index,city1['name'],city2['name'],distance)
    q.put('done')
    return
    
def get_distances():
    between_two_cities=pd.DataFrame()
    for i in range(len(cities_df)):        
        for j in range(i+1,len(cities_df)):
            city1=cities_df.iloc[i]
            city2=cities_df.iloc[j]
            distance=calculate_distance((city1['lat'],city1['lon']),(city2['lat'],city2['lon']))
            cdf=pd.DataFrame({'city1':city1['name'],
                            'city1_state':city1['state_abbr'],
                            'city2':city2['name'],
                            'city2_state':city2['state_abbr'],
                            'distance':distance},
                            index=[0])
            between_two_cities=pd.concat([between_two_cities,cdf],ignore_index=True)
            if j%1000==0:
                print(j,city1['name'],city2['name'],distance)
    return between_two_cities
def threadtest():
    qu=Queue()
    threads=[]
    between_two_cities=pd.DataFrame()
    for i in range(len(cities_df)):
        thread=Thread(target=distance_thread,args=(qu,i,cities_df))
        threads.append(thread)
        thread.start()

    while True:
        result=qu.get()
        if isinstance(result,dict):
            cdf=pd.DataFrame(result,index=[0])
            between_two_cities=pd.concat([between_two_cities,cdf],ignore_index=True)
        if result=='done':
            break
        #print(result)
    #thread.join()
    print(i)
    between_two_cities.to_json('city_distances.json',orient='records',indent=2)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit()

# %% [markdown]
# # Cluster citiy distances into groups of a given kilometer range

# %%



