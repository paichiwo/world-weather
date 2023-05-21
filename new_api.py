import requests


location = 'Kielce'
API_KEY = 'abd09a6d7a764df382cf51540185ac2e'

# city, postal code response
try:
    url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={API_KEY}'
    data = requests.get(url).json
except requests.exceptions.JSONDecodeError:
    url = f'https://api.weatherbit.io/v2.0/current?postal_code={location}&key={API_KEY}'
    data = requests.get(url).json

try:
    f_url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={API_KEY}'
    f_data = requests.get(url).json
except requests.exceptions.JSONDecodeError:
    f_url = f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={location}&key={API_KEY}'
    f_data = requests.get(url).json

print(data)
print(f_data)
