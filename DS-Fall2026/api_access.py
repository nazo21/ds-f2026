import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('KROGER_CLIENT_ID')
secret_kroger_key = os.getenv('KROGER_CLIENT_SECRET')

# api-ce.kroger.com is the certification sandbox; api.kroger.com is production.
API_HOST = os.getenv('KROGER_API_HOST', 'https://api.kroger.com')
TOKEN_URL = f'{API_HOST}/v1/connect/oauth2/token'


def get_access_token(scope='product.compact'):
    response = requests.post(
        TOKEN_URL,
        auth=(client_id, secret_kroger_key),
        data={'grant_type': 'client_credentials', 'scope': scope},
    )
    response.raise_for_status()
    return response.json()['access_token']


if __name__ == '__main__':
    access_token = get_access_token()
    print(access_token)
