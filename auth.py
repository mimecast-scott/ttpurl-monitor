import requests
import os

AUTH_URL = 'https://api.services.mimecast.com/oauth/token'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def get_bearer_token(auth_url=AUTH_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
    print("Requesting new bearer token")
    auth_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    auth_response = requests.post(auth_url, data=auth_data)
    auth_response.raise_for_status()

    return auth_response.json()['access_token']
