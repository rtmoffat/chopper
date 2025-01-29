import requests
import json
import traceback

url = "https://data.pollstar.com/data/v1/artists/1068/events"

artists=json.load(open('pollstar_artists.json'))

params={
    "page": 0,
    "pageSize": 5,
    "fromDate": "01-28-2025",
    "toDate": "01-28-2029",
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

def update_tourdates(artists,data):
    for artist in artists:
        data.append(artist['name'])
        data[artist['name']]={}
        print("Getting tourdates for",artist['name']) 
        res=get_tourdates(artist,params,headers)
        data[artist['name']]=res
    json.dump(data, open('pollstar.json', 'w'))

def condense_tourdates(tourdatesFile='pollstar.json'):
    data=json.load(open(tourdatesFile))
    for tourdates in data:
        for event in data['events']:

            condensed=[]
            for artist in data:
                for event in artist['data']:
                    condensed.append({
                        'artist':event['artistName'],
                        'date':event['playdate'],
                        'venue':event['venueName'],
                        'city':event['city'],
                        'state':event['state'],
                        'country':event['country']
                    })
            json.dump(condensed, open('pollstar_condensed.json', 'w'))
#response = requests.request("GET", url, headers=headers, params=params)
#data.append(response.json())
#print(response.text)
data={}
update_tourdates(artists,data)
#condense_tourdates()
