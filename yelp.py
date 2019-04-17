import requests
import json
import secrets
#import api_info
import yelp_api


def makeRequestUsingCache(url, params, headers):
    ident = params['location']
    try:
        cache_file1 = open('cache-yelp.json', 'r')
        cache_contents1 = cache_file1.read()
        CACHE_DICTION1 = json.loads(cache_contents1)
        cache_file1.close()
    except:
        CACHE_DICTION1 = {}
    if ident in CACHE_DICTION1:
        return CACHE_DICTION1[ident]
    else:
        response = requests.get(url, params=params, headers=headers)
        CACHE_DICTION1[ident] = response.text
        dumpJSONCache = json.dumps(CACHE_DICTION1)
        f1 = open('cache-yelp.json', 'w')
        f1_ = f1.write(dumpJSONCache)
        f1.close()
    return CACHE_DICTION1[ident]
    #return CACHE_DICTION1

def yelpRequest(city):
    header = {'Authorization': "Bearer %s" % yelp_api.yelp_api_key}
    params= {}
    params['limit'] = 20
    params['location'] = city
    url = 'https://api.yelp.com/v3/events'
    response = makeRequestUsingCache(url, params=params, headers=header)
    data = json.loads(response)
    # for event in response:
    return data
    #print(data)
    # #data = json.loads(response)
    # for city in json.dumps(response):
    #     #length = city['\"events\"']
    #     list_ = city['events']
    #     # length = len(city)
    #     # print(length)
    #     for event in range(len(list_)):
    #         print(event['attending_count'])
    #     #     print(event)
    #     #print(city)
    #     # for event in len(city):
    #     #     print(event['attending_count'])
    #     # print(city['events'])
    # #return response
    
# print(yelpRequest('New York'))
# print(yelpRequest('Ann Arbor'))
# print(yelpRequest('Miami'))
# print(yelpRequest('Los Angeles'))

def parseJSON(listOfCities):
    for city in listOfCities:
        yelpRequest(city)

    json_file = open('cache-yelp.json', 'r')
    json_str = json_file.read()
    data = json.loads(json_str)
    json_file.close()

    for x in data:
        for time in range(20):
            print(x[time])
        #print(type(x))
    
print(parseJSON(['New York', 'Ann Arbor', 'Miami', 'Los Angeles']))

# def parseData():
#     newYork = yelpRequest('New York')
#     data = json.load(open('cache-yelp.json'))
#     for city in data:
#         time = 0
#         #print(type(city))
#         for event in city[time]:
#             time += 1
#             print(event)
#         #print(info)
#     #print(data)
#     # #print(type(json.dumps(newYork)))
#     # for event in json.dumps(newYork):
#     #     print(event)
#     # # yelpRequest('Ann Arbor')
#     # # yelpRequest('Miami')
#     # # yelpRequest('Los Angeles')

# # yelp = request.get('https://api.yelp.com/v3/events' + api_info.yelp_api_key, params= url_params)
# print(parseData())

def yelp_db():
    conn = sqlite3.connect('yelpEvents.db')
    cur = conn.cursor()
    statement = '''
        DROP TABLE IF EXISTS 'Top 20 Events in Cities'
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Top 20 Events in Cities' (
            'City' = TEXT
            'Event Name' = TEXT,
            'Attendance Count' = INTEGER,
            'Cost' = INTEGER
        );
    '''
    cur.execute(statement)

def yelpInsertData():
    conn = sqlite3.connect('yelpEvents.db')
    cur = conn.cursor()