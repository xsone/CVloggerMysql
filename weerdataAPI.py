import urllib, json
# Let er even op dat je je key aanpast
key = "cae4b523b653c7c6fb64ef65a1badcbe"
plaats = "Amsterdam"
url = "http://api.openweathermap.org/data/2.5/weather?q=" + plaats + "&appid=" + key + "&units=metric"
response = urllib.urlopen(url)
data = json.loads(response.read())
temp = data['main']['temp']
print (temp)