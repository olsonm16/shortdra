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

def test_malformed_add_wrongtype(key, link, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/add/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/add/"
    d = {}
    d['link'] = link
    d['string'] = key
    response = requests.get(r, data=d)
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

def test_delete_success(key, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/delete/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/delete/"
    d = {}
    d['string'] = key
    response = requests.delete(r, data=d)
    response_data = response.json()
    if response.status_code == 200:
        if local:
            print("Link with key: " + key + " was deleted locally")
        else:
            print("Link with key: " + key + " was deleted in production")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 200")
        return False

def test_delete_failure(key, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/delete/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/delete/"
    d = {}
    d['string'] = key
    response = requests.delete(r, data=d)
    response_data = response.json()
    if response.status_code == 422:
        if local:
            print("Link with key: " + key + " was NOT deleted locally")
        else:
            print("Link with key: " + key + " was NOT deleted in production")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 422")
        return False

def test_malformed_delete(key, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/delete/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/delete/"
    d = {}
    d['asdf'] = key
    response = requests.delete(r, data=d)
    response_data = response.json()
    if response.status_code == 400:
        if local:
            print("Link with key: " + key + " was NOT deleted locally")
        else:
            print("Link with key: " + key + " was NOT deleted in production")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 400")
        return False

def test_malformed_delete_wrongtype(key, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/delete/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/delete/"
    d = {}
    d['string'] = key
    response = requests.put(r, data=d)
    response_data = response.json()
    if response.status_code == 400:
        if local:
            print("Link with key: " + key + " was NOT deleted locally")
        else:
            print("Link with key: " + key + " was NOT deleted in production")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 400")
        return False

def test_avail_check(key, local=False):
    if local:
        r = "http://127.0.0.1:8000/api/v1/shortdra/avail/"
    else:
        r = "http://shortdra.hydr.as/api/v1/shortdra/avail/"
    d = {}
    d['string'] = key
    response = requests.get(r, data=d)
    response_data = response.json()
    if response.status_code == 200:
        if local:
            print("Key: " + key + " is available locally.")
        else:
            print("Key: " + key + " is available in production.")
        print(response)
        print("API returns message: " + response_data['body']['message'] + " with status " + response_data['status_code'])
        return True
    else:
        print("The status code was not 200")
        return False  
    
def create_random_key(n):
    key = ""
    i = 0
    while i < n:
        index = random.randint(0, 25)
        key += ALPHABET[index]
        i += 1
    return key

def run_tests(local=False):
    success_key = create_random_key(15)
    fail_key = create_random_key(15)
    width = len("_________Running Test Suite on Add Shortlink API_________")
    """

    print("\n_________Running Test Suite on Add Shortlink API_________\n")

    print("Testing successful add")
    assert test_successful_add(success_key, "google.com", local)
    print("\n" + "_"*width + "\n")

    print("Testing key taken failure")
    assert test_keytaken_add(success_key, "google.com", local)
    print("\n" + "_"*width + "\n")

    print("Testing malformed add request with bad field")
    assert test_malformed_add(success_key, "google.com", local)
    print("\n" + "_"*width + "\n")

    print("Testing malformed add request with incorrect GET request type")
    assert test_malformed_add_wrongtype(success_key, "google.com", local)
    print("\n" + "_"*width + "\n")

    print("_________Running Test Suite on Delete Shortlink API_________\n")

    print("Testing successful delete")
    assert test_delete_success(success_key, local)
    print("\n" + "_"*width + "\n")

    print("Testing failed delete (key doesn't exist)")
    assert test_delete_failure(fail_key, local)
    print("\n" + "_"*width + "\n")

    print("Testing malformed delete request with bad field")
    assert test_malformed_delete(success_key, local)
    print("\n" + "_"*width + "\n")

    print("\n_________Running Test Suite on Available Check Shortlink API_________\n")

    print("Testing malformed delete request with incorrect PUT request type")
    assert test_malformed_delete_wrongtype(success_key, local)
    print("\n" + "_"*width + "\n")
    """

    print("Testing successful avail check")
    assert test_avail_check(success_key, local)
    print("\n" + "_"*width + "\n")

    print("All tests passed.")

def localServerUp():
    r = "http://127.0.0.1:8000/"
    try:
        k =requests.get(r, data={})
        return True
    except:
        return False


if localServerUp():
    run_tests(local=True)
run_tests()

