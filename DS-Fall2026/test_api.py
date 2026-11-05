"""Check that the Kroger API credentials work end to end.

Run with:  ./.venv/bin/python test_api.py
"""

import pandas as pd

import api_access


def main():
    print(f'Host: {api_access.API_HOST}')

    print('\n[1/3] Credentials loaded from .env ...')
    if not api_access.client_id or not api_access.secret_kroger_key:
        print('  FAIL: KROGER_CLIENT_ID / KROGER_CLIENT_SECRET not set')
        return
    print(f'  ok (client_id is {len(api_access.client_id)} chars)')

    print('\n[2/3] Requesting access token ...')
    try:
        token = api_access.get_access_token()
    except RuntimeError as exc:
        print(f'  FAIL: {exc}')
        print('\n  Get new credentials at https://developer.kroger.com')
        return
    print(f'  ok (token is {len(token)} chars)')

    print('\n[3/3] Searching products for "milk" ...')
    try:
        products = api_access.search_products(token, 'milk')
    except RuntimeError as exc:
        print(f'  FAIL: {exc}')
        return

    rows = [
        {
            'productId': p.get('productId'),
            'brand': p.get('brand'),
            'description': p.get('description'),
        }
        for p in products
    ]
    print(f'  ok ({len(rows)} results)\n')
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == '__main__':
    main()
