import sys
import requests

URL = 'http://127.0.0.1:8000/api/v1/shortdra/add/'

client = requests.session()

# Retrieve the CSRF token first
client.get(URL)  # sets cookie
print(client.cookies)
csrftoken = client.cookies['csrftoken']

print(csrftoken)

request = {}
request['string'] = "mydstring"
request['url'] = "google.com"
request['csrfmiddlewaretoken'] = csrftoken
request['next']='/'
r = client.post(URL, data=request, headers=dict(Referer=URL))
print(r.text)