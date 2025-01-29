import requests
import json
import traceback

url = "https://data.pollstar.com/data/v1/artists/1068/events"

artists=json.load(open('pollstar_artists.json'))

params={
    "page": 0,
    "pageSize": 50,
    "fromDate": "01-29-2025",
    "toDate": "01-29-2029",
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
#response = requests.request("GET", url, headers=headers, params=params)
#data.append(response.json())
#print(response.text)
url = "https://data.pollstar.com/data/v1/artists/1068/events"

artists=json.load(open('pollstar_artists.json'))
update_tourdates(artists)
condense_tourdates()
