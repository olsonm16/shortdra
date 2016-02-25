import requests
import string
import random

ALPHABET = string.ascii_lowercase

def test_successful_add(key, link, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/add/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/add/"
    d = {}
    d['link'] = link
    d['string'] = key
    response = requests.post(r, data=d)
    response_data = response.json()
    if response.status_code == 200:
        if local:
            print("New link with key: " + key + " created locally")
        else:
            print("New link with key: " + key + " created in production")
        print("Mapping between " + key + " -> " + link + " is now defined")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 200")
        return False

def test_keytaken_add(key, link, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/add/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/add/"
    d = {}
    d['link'] = link
    d['string'] = key
    response = requests.post(r, data=d)
    response_data = response.json()
    if response.status_code == 422:
        if local:
            print("New link with key: " + key + " was not created locally")
        else:
            print("New link with key: " + key + " was not created in production")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 422")
        return False   

def test_malformed_add(key, link, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/add/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/add/"
    d = {}
    d['asdf'] = link
    d['string'] = key
    response = requests.post(r, data=d)
    response_data = response.json()
    if response.status_code == 400:
        if local:
            print("New link with key: " + key + " was not created locally")
        else:
            print("New link with key: " + key + " was not created in production")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 400")
        return False
    
def create_random_key(n):
    key = ""
    i = 0
    while i < n:
        index = random.randint(0, 25)
        key += ALPHABET[index]
        i += 1
    return key

def run_tests():
    success_key = create_random_key(15)
    width = len("_________Running Test Suite on Add Shortlink API_________")
    print("_________Running Test Suite on Add Shortlink API_________\n")
    print("Testing successful add")
    assert test_successful_add(success_key, "google.com", local=True)
    print("\n" + "_"*width + "\n")
    print("Testing key taken failure")
    assert test_keytaken_add(success_key, "google.com", local=True)
    print("\n" + "_"*width + "\n")
    print("Testing malformed request")
    assert test_malformed_add(success_key, "google.com", local=True)
    print("\n" + "_"*width + "\n")


run_tests()
        
        
    
