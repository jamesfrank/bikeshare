import xml.etree.ElementTree as et
import urllib.request

# config
url = 'https://www.capitalbikeshare.com/data/stations/bikeStations.xml'
terminals = [31619, 31623]

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

    name = station.find('./name').text
    bikes = station.find('./nbBikes').text
    docks = station.find('./nbEmptyDocks').text

    print(name)
    print(bikes, 'bikes')
    print(docks, 'available slots', end='\n\n')
