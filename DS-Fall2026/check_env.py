"""Diagnose .env formatting and try the token endpoint on both Kroger hosts.

Never prints a full secret - only lengths and a short masked preview.
Run with:  ./.venv/bin/python check_env.py
"""

import os

import requests
from dotenv import load_dotenv

HOSTS = ['https://api.kroger.com', 'https://api-ce.kroger.com']


def mask(value):
    return f'{value[:6]}...{value[-4:]}' if len(value) > 12 else '<short>'


def inspect_file(path='.env'):
    raw = open(path, 'rb').read()
    print(f'{path}: {len(raw)} bytes | CRLF: {b"\r\n" in raw} | '
          f'BOM: {raw.startswith(b"\xef\xbb\xbf")}')

    for i, line in enumerate(raw.decode('utf-8', 'replace').splitlines(), 1):
        if not line.strip():
            print(f'  line {i}: <blank>')
            continue
        if line.lstrip().startswith('#'):
            print(f'  line {i}: <comment>')
            continue
        if '=' not in line:
            print(f'  line {i}: NO "=" SIGN -- malformed')
            continue

        key, value = line.split('=', 1)
        issues = []
        if key != key.strip():
            issues.append('whitespace around key')
        if value != value.strip():
            issues.append('leading/trailing whitespace')
        if value[:1] in ('"', "'") or value[-1:] in ('"', "'"):
            issues.append('wrapped in quotes')

        clean = value.strip().strip('"\'')
        print(f'  line {i}: {key.strip():20} len={len(clean):4} '
              f'{mask(clean):16} {", ".join(issues) or "clean"}')


def try_hosts():
    client_id = os.getenv('KROGER_CLIENT_ID')
    secret = os.getenv('KROGER_CLIENT_SECRET')
    if not client_id or not secret:
        print('\nCredentials not loaded - fix .env first.')
        return

    print('\nTrying token endpoint on both environments:')
    for host in HOSTS:
        try:
            response = requests.post(
                f'{host}/v1/connect/oauth2/token',
                auth=(client_id, secret),
                data={'grant_type': 'client_credentials',
                      'scope': 'product.compact'},
                timeout=15,
            )
        except requests.RequestException as exc:
            print(f'  {host:32} network error: {exc}')
            continue

        verdict = 'SUCCESS' if response.ok else response.text[:90]
        print(f'  {host:32} {response.status_code} {verdict}')


if __name__ == '__main__':
    inspect_file()
    load_dotenv()
    try_hosts()
