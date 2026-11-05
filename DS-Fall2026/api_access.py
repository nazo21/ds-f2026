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
    if not client_id or not secret_kroger_key:
        raise RuntimeError(
            'KROGER_CLIENT_ID / KROGER_CLIENT_SECRET missing from .env'
        )
    response = requests.post(
        TOKEN_URL,
        auth=(client_id, secret_kroger_key),
        data={'grant_type': 'client_credentials', 'scope': scope},
    )
    if not response.ok:
        raise RuntimeError(
            f'Token request failed: {response.status_code} {response.text}'
        )
    return response.json()['access_token']


def search_products(token, term, location_id=None, limit=5):
    params = {'filter.term': term, 'filter.limit': limit}
    if location_id:
        params['filter.locationId'] = location_id
    response = requests.get(
        f'{API_HOST}/v1/products',
        headers={'Authorization': f'Bearer {token}'},
        params=params,
    )
    if not response.ok:
        raise RuntimeError(
            f'Product search failed: {response.status_code} {response.text}'
        )
    return response.json()['data']


if __name__ == '__main__':
    access_token = get_access_token()
    print(access_token)
