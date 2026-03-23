import IP2Location
database = IP2Location.IP2Location("IP2LOCATION-LITE-DB3.BIN")
print(database.get_all('8.8.8.8'))
