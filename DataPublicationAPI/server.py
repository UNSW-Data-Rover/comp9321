from flask import Flask, request, jsonify
import json, csv, os, requests
from bs4 import BeautifulSoup
import urllib.request
from pymongo import MongoClient


app = Flask(__name__)


@app.route('/getallevents/', methods=['GET'])
def getallevents():
    rows = []
    with open('DataPublicationAPI/WorldCups.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.extend([{'Year': row['Year'], 'Country': row['Country'], 'Champion': row['Winner'],
                          'Runners-Up': row['Runners-Up'], 'Third': row['Third'], 'Fourth': row['Fourth'],
                          'TotalGoals': row['GoalsScored'], 'QualifiedTeams': row['QualifiedTeams'],
                          'MatchesPlayed': row['MatchesPlayed'],'Attendance': row['Attendance']}])
    ##with open('static/events.json', 'w') as f:
        ##f.write(json.dumps(rows, sort_keys=False, indent=4, separators=(',', ': ')))
    client = MongoClient('mongodb://datarover:datarover@ds113775.mlab.com:13775/9321')
    db = client.get_database()
    allcups = db['allcups']
    if allcups.find().count() == 0:
        for item in rows:
            allcups.insert_one(item)
    else:
        pass
    data = allcups.find()
    cup_dict = []
    for item in data:
        item.pop('_id')
        cup_dict.append(item)
    return jsonify(cup_dict),{'Access-Control-Allow-Origin': '*'}
     ##with open('static/events.json', 'r') as f:
        ##load_dict = json.load(f)
        ##return jsonify(load_dict)


@app.route('/getfinalstats/', methods=['GET'])
def getfinalstats():
    rows = []
    result = []
    with open('DataPublicationAPI/WorldCupMatches.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Stage'] == 'Final':
                rows.extend([{'Year': row['Year'], 'Stage': row['Stage'], 'Home Team': row['Home Team Name'],
                                  'Home Team Goals': row['Home Team Goals'], 'Away Team Goals': row['Away Team Goals'],
                                  'Away Team': row['Away Team Name'], }])
    ##with open('static/matches.json', 'w') as f:
        ##f.write(json.dumps(rows, sort_keys=False, indent=4, separators=(',', ': ')))
    client = MongoClient('mongodb://datarover:datarover@ds113775.mlab.com:13775/9321')
    db = client.get_database()
    allfinals = db['allfinals']
    if allfinals.find().count() == 0:
        for item in rows:
            allfinals.insert_one(item)
    else:
        pass
    data = allfinals.find()
    final_dict = []
    for item in data:
        item.pop('_id')
        final_dict.append(item)
    return jsonify(final_dict),{'Access-Control-Allow-Origin': '*'}
    ##with open('static/matches.json', 'r') as f:
        ##load_dict = json.load(f)
        ##for item in load_dict:
            ##if item['Stage'] == 'Final':
                ##result.append(item)
        ##return jsonify(result)


@app.route('/querybycountry/<country>', methods=['GET'])
def querybycountry(country):
    region = None
    if country == 'USA':
        region = 'United%20States%20of%20America'
    elif country == 'Czechoslovakia':
        region = 'Czech%20Republic'
    elif country == 'Germany FR':
        region = 'Germany'
    elif country == 'Korea Republic':
        region = 'Republic%20of%20Korea'
    elif country == 'Soviet Union':
        region = 'Russian%Federation'
    elif country == 'England':
        region = 'United%20Kingdom'
    else:
        region = country
    url = 'http://data.un.org/CountryProfile.aspx/en/index.html/CountryProfile.aspx?crName=' + region
    with urllib.request.urlopen(url) as response:
        html_data = response.read()
    table_data = [[cell.text for cell in row('td')]
                  for row in BeautifulSoup(html_data, 'html.parser')('tr')]
    ##print(table_data)
    wanted = ['Region', 'Surface area (sq km)', 'Population (proj., 000)', 'Pop. density (per sq km)',
              'Capital city', 'Currency', 'UN membership date']
    new_dict = {}
    for item in table_data:
        if len(item) > 2 and item[0] in wanted:
            if item[0] == 'Population (proj., 000)':
                new_dict['Population (proj, 000)'] = item[2]
            elif item[0] == 'Pop. density (per sq km)':
                new_dict['Pop density (per sq km)'] = item[2]
            else:
                new_dict[item[0]] = item[2]
    new_dict['Country'] = country
    client = MongoClient('mongodb://datarover:datarover@ds113775.mlab.com:13775/9321')
    db = client.get_database()
    countrys = db['countrys']
    if countrys.find({'Country':country}).count() > 0:
        pass
    else:
        countrys.insert_one(new_dict)
    data = countrys.find({'Country':country})
    country_dict = []
    for item in data:
        item.pop('_id')
        country_dict.append(item)
    return jsonify(country_dict),{'Access-Control-Allow-Origin': '*'}
    ##filename = 'static/' + country + '.json'
    ##with open(filename, 'w') as f:
        ##f.write(json.dumps(new_dict, sort_keys=False, indent=4, separators=(',', ': ')))
    ##with open(filename, 'r') as f:
        ##load_dict = json.load(f)
        ##return jsonify(load_dict)


##def download_data():
    ##kaggle_info = {'UserName':'datarover', 'Password':'datarover'}
    ##data_urls = []


if __name__ == '__main__':
    app.run()