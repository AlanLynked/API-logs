import urllib.request
import json

url = 'http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s'
app_id = 'f54b3acfe7e3f8e3cc84d983c918f3a0'


def get_data():
    """
    Requests city name from user, then performs API request to openweathermap.org
    In successful cases returns service response as JSON packed to dict.
    @return: None or dict
    """
    city = input()
    js = None
    try:
        req = urllib.request.urlopen(url % (city, app_id))
        js = json.loads(req.read().decode())
    finally:
        return js


print('Please enter the city name')
response = get_data()

# Adding the exit option and the ability to repeat request in case of unsuccessful execution
while not response:
    print('Incorrect city name! Please try again or you can quit by pressing Ctrl+C')
    try:
        response = get_data()
    except KeyboardInterrupt:
        print('Exit...')
        exit()

print(f"{response['main']['temp']} °C" )
