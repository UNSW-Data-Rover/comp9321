import googlemaps
from flask import Flask
import requests
import json
import urllib
from urllib.request import urlopen
import csv
from flask import jsonify
import sys,io
from flask_cors import CORS
from flask_restful import reqparse
from datetime import datetime
from pymongo import MongoClient


local_file={}

class Country:
    def __init__(self, name):
        self.name = name


response1=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyDlJxbn3xmDZxX3Seek-wwSalU6hXQKsqQ')
gmaps = googlemaps.Client(key='AIzaSyDlJxbn3xmDZxX3Seek-wwSalU6hXQKsqQ')
app = Flask(__name__)
CORS(app)
# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')


def get(address):
    addressUrl='https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key=AIzaSyDlJxbn3xmDZxX3Seek-wwSalU6hXQKsqQ'
    addressUrlQuote = urllib.parse.quote(addressUrl, ':?=/')
    response = urlopen(addressUrl).read().decode('utf-8')
    responseJson = json.loads(response)
    if responseJson.get('status') == "OK":
        lat = responseJson.get('results')[0]['geometry']['location']['lat']
        lng = responseJson.get('results')[0]['geometry']['location']['lng']
        return str(lat)+','+str(lng)

def getaddress(address):
    addressUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=AIzaSyDlJxbn3xmDZxX3Seek-wwSalU6hXQKsqQ'
    addressUrlQuote = urllib.parse.quote(addressUrl, ':?=/')
    response = urlopen(addressUrl).read().decode('utf-8')
    responseJson = json.loads(response)
    if responseJson.get('status')=="OK":
        return responseJson.get('results')[0]['formatted_address']

def getstadium():
    filename='WorldCupMatches.csv'
    dic=[]
    with open(filename,'r') as f:
        reader = csv.DictReader(f)
        L0 = [row['Year'] for row in reader]
    with open(filename, 'r') as f1:
        reader1 = csv.DictReader(f1)
        L1 = [row['Stadium'] for row in reader1]
    for i in range(len(L0)):
        dic.append([L0[i],L1[i]])
    return dic


l=getstadium()
for i in l:
    if i[0]=='1930':
        i[0]='Uruguay'
    elif i[0]=='1934':
        i[0]='Italy'
    elif i[0] == '1938':
        i[0] = 'France'
    elif i[0]=='1950':
        i[0]='Brazil'
    elif i[0]=='1954':
        i[0]='Switzerland'
    elif i[0]=='1958':
        i[0]='Sweden'
    elif i[0]=='1962':
        i[0]='Chile'
    elif i[0]=='1966':
        i[0]='England'
    elif i[0]=='1970':
        i[0]='Mexico'
    elif i[0]=='1974':
        i[0]='Germany'
    elif i[0]=='1978':
        i[0]='Argentina'
    elif i[0]=='1982':
        i[0]='Spain'
    elif i[0]=='1986':
        i[0]='Mexico'
    elif i[0]=='1990':
        i[0]='Italy'
    elif i[0]=='1994':
        i[0]='USA'
    elif i[0]=='1998':
        i[0]='France'
    elif i[0]=='2002':
        i[0]='Korea&Japan'
    elif i[0]=='2006':
        i[0]='Germany'
    elif i[0]=='2010':
        i[0]='SouthAfrica'
    elif i[0]=='2014':
        i[0]='Brazil'


# getaddress('GiorgioAscarelli')
p=[]
p1=[]
p2=[]
p3=[]
n=[]
for k in l:
    p.append(k[0])
    p1.append(k[1])
dic1=dict(zip(p1,p))
for key,value in dic1.items():
    p2.append(key)
    p3.append(value)
for h in range(len(p2)):
    n.append([p3[h], p2[h]])



# getstadium()
# get('austrilia')
@app.route("/country/<name>", methods=['GET'])
def get_result(name):
    # parser = reqparse.RequestParser()
    # parser.add_argument('countryname', type=str)
    # args = parser.parse_args()
    #
    # name = args.get("countryname")
   
    m=[]
    name1=name.replace(' ','')

    client = MongoClient('mongodb://DBLiang:1234@ds249249.mlab.com:49249/9321lab7')
    db = client.get_database()
    googledb = db['googleMap']

    new_dict={}
    if googledb.find({'Country': name1}).count() > 0:
    	print('gotcha')
    	data = googledb.find({'Country': name1})
    	country_dict = []
    	for item in data:
    		item.pop('_id')
    		country_dict.append(item)

    	wanted= country_dict[0]['data']
    	return jsonify(wanted)

    for i in n:
        if i[0]==name1:
            j=i[1].replace(' ','')
            response = {"Stadium": j,"Address": getaddress(j),'Coordinate': get(j)}
            m.append(response)
            # d=dict([('Stadium',i[1]),('Address',getaddress(i[1])), ('Coordinate',get(i[1]))])
    m.append({'Country Coordinate':get(name1)})
    # print(m)
    new_dict['Country']= name1
    new_dict['data']=m
    googledb.insert_one(new_dict)


    return jsonify(m)

#
if __name__ == "__main__":
    app.run(port=8080)
