from flask import Flask, request, jsonify
import json, csv, os, requests
from bs4 import BeautifulSoup
import urllib.request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/getallevents/', methods=['GET'])
def getallevents():
    rows = []
    with open('WorldCups.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.extend([{'Year': row['Year'], 'Country': row['Country'], 'Champion': row['Winner'],
                          'Runners-Up': row['Runners-Up'], 'Third': row['Third'], 'Fourth': row['Fourth'],
                          'TotalGoals': row['GoalsScored'], 'QualifiedTeams': row['QualifiedTeams'],
                          'MatchesPlayed': row['MatchesPlayed'], 'Attendance': row['Attendance']}])
    ##with open('static/events.json', 'w') as f:
    ##f.write(json.dumps(rows, sort_keys=False, indent=4, separators=(',', ': ')))
    client = MongoClient('mongodb://datarover:datarover@ds113775.mlab.com:13775/9321')
    db = client.get_database()
    allcups = db['allcups']
    if allcups.find().count() == 0:
        for item in rows:
            allcups.insert_one(item)
    else:
        for item in rows:
            allcups.update_one(filter={'Year': item['Year']}, update={'$set': item})
    data = allcups.find()
    cup_dict = []
    for item in data:
        item.pop('_id')
        cup_dict.append(item)
    return jsonify(cup_dict)
    ##with open('static/events.json', 'r') as f:
    ##load_dict = json.load(f)
    ##return jsonify(load_dict)


##@app.route('/getfinalstats/', methods=['GET'])
##def getfinalstats():
##rows = []
##result = []
##with open('WorldCupMatches.csv') as f:
##reader = csv.DictReader(f)
##for row in reader:
##if row['Stage'] == 'Final':
##rows.extend([{'Year': row['Year'], 'Stage': row['Stage'], 'Home Team': row['Home Team Name'],
##'Home Team Goals': row['Home Team Goals'], 'Away Team Goals': row['Away Team Goals'],
##'Away Team': row['Away Team Name'], }])
##with open('static/matches.json', 'w') as f:
##f.write(json.dumps(rows, sort_keys=False, indent=4, separators=(',', ': ')))
##client = MongoClient('mongodb://datarover:datarover@ds113775.mlab.com:13775/9321')
##db = client.get_database()
##allfinals = db['allfinals']
##if allfinals.find().count() == 0:
##for item in rows:
## allfinals.insert_one(item)
##else:
##pass


##data = allfinals.find()
##final_dict = []
##for item in data:
##item.pop('_id')
##final_dict.append(item)
##return jsonify(final_dict)

@app.route('/getstats/<countries>', methods=['GET'])
def getstats(countries):
    rows = []
    result = []
    first_country = countries.split('&')[0]
    second_country = countries.split('&')[1]
    with open('WorldCupMatches.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row['Home Team Name'] == first_country and row['Away Team Name'] == second_country) \
                    or (row['Home Team Name'] == second_country and row['Away Team Name'] == first_country):
                rows.extend([{'Year': row['Year'], 'Stage': row['Stage'], 'Home Team': row['Home Team Name'],
                              'Home Team Goals': row['Home Team Goals'], 'Away Team Goals': row['Away Team Goals'],
                              'Away Team': row['Away Team Name'], }])
    victory_1 = 0
    victory_2 = 0
    for row in rows:
        if row['Home Team'] == first_country and int(row['Home Team Goals']) > int(row['Away Team Goals']):
            victory_1 += 1
        elif row['Away Team'] == first_country and int(row['Away Team Goals']) > int(row['Home Team Goals']):
            victory_1 += 1
        elif row['Away Team'] == second_country and int(row['Away Team Goals']) > int(row['Home Team Goals']):
            victory_2 += 1
        elif row['Home Team'] == second_country and int(row['Home Team Goals']) > int(row['Away Team Goals']):
            victory_2 += 1
    print(victory_2)
    winning_1 = victory_1 / len(rows)
    winning_2 = victory_2 / len(rows)

    winning_rate = {
        'winnings': {first_country + ' winning rate': round(winning_1, 2), second_country + ' winning rate': round(winning_2, 2)}}
    print(winning_rate)
    rows.extend([winning_rate])

    CountryCode = {}
    if first_country == 'Korea Republic':
        first_country = 'Republic of Korea'
    if first_country == 'Soviet Union':
        region = 'Russian Federation'
    if first_country == 'Russia':
        region = 'Russian Federation'
    if second_country == 'Korea Republic':
        first_country = 'Republic of Korea'
    if second_country == 'Soviet Union':
        region = 'Russian Federation'
    if second_country == 'Russia':
        region = 'Russian Federation'
    with open('CountryCode.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['CountryName'] == first_country:
                print(row['CountryCode'])
                CountryCode['FirstCode'] = row['CountryCode']
            if row['CountryName'] == second_country:
                print(row['CountryCode'])
                CountryCode['SecondCode'] = row['CountryCode']
    temp = {'CountryCode':CountryCode}
    rows.extend([temp])

    client = MongoClient('mongodb://datarover:datarover@ds113775.mlab.com:13775/9321')
    db = client.get_database()
    versus = db[countries]
    if versus.find().count() == 0:
        for item in rows:
            versus.insert_one(item)
    else:
        for item in rows[:-2]:
            versus.update_one(filter={'Year': item['Year']}, update={'$set': item})
        versus.update_one(filter={'winnings': 'winnings'}, update={'$set': rows[-2]})
        versus.update_one(filter={'CountryCode': 'CountryCode'}, update={'$set': rows[-1]})
    data = versus.find()
    final_dict = []
    for item in data:
        item.pop('_id')
        final_dict.append(item)
    return jsonify(final_dict)


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
    elif country == 'England':
        region = 'United%20Kingdom'
    elif country == 'Soviet Union':
        region = 'Russian%20Federation'
    elif country == 'Russia':
        region = 'Russian%20Federation'
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
    realname = ''
    if len(region.split('%20')) > 1:
        for item in region.split('%20'):
            realname = realname + ' ' + item
        realname = realname.lstrip()
    else:
        realname = region
    print(realname)
    with open('CountryCode.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['CountryName'] == realname:
                print(region)
                print(row['CountryCode'])
                new_dict['CountryCode'] = row['CountryCode']

    client = MongoClient('mongodb://datarover:datarover@ds113775.mlab.com:13775/9321')
    db = client.get_database()
    countrys = db['countrys']
    if countrys.find({'Country': country}).count() > 0:
        countrys.update_one(filter={'Country': new_dict['Country']}, update={'$set': new_dict})
    else:
        countrys.insert_one(new_dict)
    data = countrys.find({'Country': country})
    country_dict = []
    for item in data:
        item.pop('_id')
        country_dict.append(item)
    return jsonify(country_dict)


##def download_data():
##kaggle_info = {'UserName':'datarover', 'Password':'datarover'}
##data_urls = []


if __name__ == '__main__':
    app.run()
