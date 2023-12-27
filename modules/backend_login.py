import requests
import json


def login(username, password):
    url = "https://api.ameasere.com/polaris/login"
    payload = json.dumps({"username": username, "password": password})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)
    # Get the response and code - the response should have text, not just <Response [code]>
    response_code = response.status_code
    response_text = response.text
    try:
        return json.loads(response_text), response_code
    except json.decoder.JSONDecodeError:
        return response_text, response_code


def device_token(username, password, rt=None):
    url = "https://api.ameasere.com/polaris/device_token"
    payload = json.dumps(
        {"username": username, "password": password, "2fa_rt": rt})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)
    # Get the response and code - the response should have text, not just <Response [code]>
    response_code = response.status_code
    response_text = response.text
    try:
        return json.loads(response_text), response_code
    except json.decoder.JSONDecodeError:
        return response_text, response_code


def token_login(password, token):
    url = "https://api.ameasere.com/polaris/token_login"
    payload = json.dumps({"password": password, "token": token})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)
    # Get the response and code - the response should have text, not just <Response [code]>
    response_code = response.status_code
    response_text = response.text
    try:
        return json.loads(response_text), response_code
    except json.decoder.JSONDecodeError:
        return response_text, response_code


def two_factor(username, password, code):
    url = "https://api.ameasere.com/polaris/2fa"
    payload = json.dumps({"username": username, "password": password, "code": code})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)
    # Get the response and code - the response should have text, not just <Response [code]>
    response_code = response.status_code
    response_text = response.text
    try:
        return json.loads(response_text), response_code
    except json.decoder.JSONDecodeError:
        return response_text, response_code
