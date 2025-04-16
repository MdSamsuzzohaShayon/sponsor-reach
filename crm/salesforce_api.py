# crm/salesforce_api.py

import requests
import os
import json

TOKEN_FILE = "salesforce_token.json"


def get_salesforce_access_token():
    """
    Fetch a new Salesforce access token using client credentials,
    and save it locally in salesforce_token.json.
    """
    url = f"{os.getenv('SALESFORCE_API_URL')}/oauth2/token"
    client_id = os.getenv("SALESFORCE_CLIENT_ID")
    client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    token_data = response.json()

    save_token(token_data["access_token"])
    return token_data["access_token"]


def save_token(access_token):
    """
    Save the access token to a local JSON file.
    """
    token_data = {
        "access_token": access_token
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)


def load_token():
    """
    Load the access token from the local JSON file.
    Returns None if the file doesn't exist.
    """
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)["access_token"]
    return None
