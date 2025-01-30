import requests
import json
import traceback
from datetime import datetime,timedelta



#url = "https://data.pollstar.com/data/v1/artists/1068/events"

artists=json.load(open('pollstar_artists.json'))
now=datetime.now()
fromDate=now.strftime("%m-%d-%Y")
toDate=now+timedelta(days=365)
toDate=toDate.strftime("%m-%d-%Y")

print(artists,fromDate,toDate)
params={
    "page": 0,
    "pageSize": 50,
    "fromDate": fromDate,
    "toDate": toDate,
    "sortAscending": "true",
    "sortColumn": "playdate",
    "newOnly": "false"
}

#payload = {}

headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'no-cache',
  'content-type': 'application/json',
  'origin': 'https://www.pollstar.com',
  'pragma': 'no-cache',
  'referer': 'https://www.pollstar.com/'
}

def get_tourdates(artist,params,headers):
    try:
        url = "https://data.pollstar.com/data/v1/artists/"+str(artist['id'])+"/events"

        response = requests.request("GET", url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        print("Error getting tourdates for",artist['name'])
        print(e.with_traceback(traceback.print_exc()))

def update_tourdates(artists):
    data={}
    for artist in artists:
        print("Getting tourdates for",artist['name']) 
        res=get_tourdates(artist,params,headers)
        data[artist['name']]=res
    json.dump(data, open('pollstar.json', 'w'),indent=5)

def condense_tourdates(tourdatesFile='pollstar.json'):
    data=json.load(open(tourdatesFile))
    condensed=[]
    for artist in data:
        print(artist)
        for event in data[artist]['events']:
            rec={"artist":artist,"date":event['playDate'],"city":event['venue']['location']}
            condensed.append(rec)
    json.dump(condensed, open('pollstar_condensed.json', 'w'),indent=5)

artists=json.load(open('pollstar_artists.json'))
update_tourdates(artists)
condense_tourdates()
