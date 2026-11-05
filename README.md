# DSA 230 Recipe & Grocery Planner — Team Setup

This guide gets your machine ready to work on the project. Follow every step before you write any code.

## 1. Get your own Kroger API key

Everyone registers their **own** free key. Do not share keys in chat, email, or code.

A key is tied to one developer account. If we share one key, one person's mistakes count against everyone's daily rate limit, and a key pushed to GitHub can be abused and get revoked.

1. Go to [developer.kroger.com](https://developer.kroger.com/) and create a developer account.
2. Register a new application (any name, e.g. `dsa230-recipes-yourname`).
3. If the form asks which APIs you need, pick **Products** and **Locations**.
4. If it asks for a redirect URI, use `http://localhost:8000/callback`. We don't use it, but the form may require one.
5. Copy your **Client ID** and **Client Secret**.

## 2. Install Python and packages

You need Python 3.10 or newer. Check with `python --version`.

```bash
pip install pandas numpy requests python-dotenv
```

## 3. Get the project folder

Clone the repo, or create this layout if you're starting fresh:

```
recipe-planner/
├── .env              # your keys — never commit
├── .gitignore
├── README.md
├── recipes.csv       # our recipe list
└── data/             # cached API results go here
```

## 4. Add your keys in a `.env` file

In the project folder, create a file named `.env` with your own values (no quotes, no spaces):

```
KROGER_CLIENT_ID=your_client_id
KROGER_CLIENT_SECRET=your_client_secret
```

## 5. Make sure `.env` is ignored by Git

Make sure `.gitignore` contains the following **before** your first commit:

```
.env
__pycache__/
.ipynb_checkpoints/
```

Run `git status`. `.env` must **not** appear in the list.

If a key ever gets committed, regenerate it in the Kroger portal right away. Deleting the file afterwards does not remove it from Git history.

## 6. Test your setup

Save this as `test_setup.py` in the project folder and run `python test_setup.py`:

```python
import os, base64, requests
from dotenv import load_dotenv

load_dotenv()
cid, secret = os.getenv("KROGER_CLIENT_ID"), os.getenv("KROGER_CLIENT_SECRET")
assert cid and secret, "Keys not found — check your .env file"

auth = base64.b64encode(f"{cid}:{secret}".encode()).decode()
r = requests.post(
    "https://api.kroger.com/v1/connect/oauth2/token",
    headers={"Authorization": f"Basic {auth}",
             "Content-Type": "application/x-www-form-urlencoded"},
    data={"grant_type": "client_credentials", "scope": "product.compact"},
)
r.raise_for_status()
token = r.json()["access_token"]

r = requests.get(
    "https://api.kroger.com/v1/locations",
    headers={"Authorization": f"Bearer {token}"},
    params={"filter.zipCode.near": "44115", "filter.limit": 1},
)
r.raise_for_status()
store = r.json()["data"][0]
print("Setup works! Nearest store:", store["name"], "-", store["locationId"])
```

If it prints a store name, you're ready.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `Keys not found` | `.env` must be in the folder you run the script from, and the names must match exactly. |
| `401 Unauthorized` | Client ID or secret is wrong. Copy them again from the Kroger portal. |
| `ModuleNotFoundError` | Rerun the `pip install` line from step 2. |
| `429 Too Many Requests` | You hit the daily rate limit. Wait, and save API results to `data/` instead of calling the API again. |
