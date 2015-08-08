import configparser
import xml.etree.ElementTree as et
import urllib.request
import datetime
import http.client, urllib

def push_message(token, user, message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": token,
                "user": user,
                "message": message,
                }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# handle config
config = configparser.ConfigParser()
config.read('config.ini')

url = config['bikeshare']['url']
terminals = list(map(int, config['bikeshare']['terminals'].split(',')))
token = config['pushover']['token']
user = config['pushover']['user']

# get data as string
data = urllib.request.urlopen(url).read()

# parse data
tree = et.fromstring(data)
stations = tree.findall('./station')

# print out stations of interest
for station in stations:
    terminal = int(station.find('./terminalName').text)
    if not terminal in terminals:
        continue

    # copy values we care about
    name = station.find('./name').text.strip() # names sometimes have extra whitespace
    bikes = int(station.find('./nbBikes').text)
    docks = int(station.find('./nbEmptyDocks').text)
    timestamp = int(station.find('./latestUpdateTime').text)

    # figure out status
    if bikes == 0:
        status = 'empty'
    elif docks == 0:
        status = 'full'
    else:
        status = 'normal'

    # print some things
    print(name)
    print(bikes, 'bikes')
    print(docks, 'available slots')
    print('Fetched', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    if not status == 'normal':
        message = name + ' is ' + status
        print(message)
        push_message(token, user, message)
    print()
