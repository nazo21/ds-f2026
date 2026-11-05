from api_access import get_access_token
import requests
import pandas as pd
import json
import numpy as np

def search_kroger(items):
    LOCATION_ID = "01400705"
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api-ce.kroger.com/v1/products"
    params = {
    "filter.term": items,            # the grocery item, e.g. "Eggs"
    "filter.locationId": "01400705",
    "filter.limit": 3,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
    print(params)
    print(response.json())  

def main():
    print("Welcome to the Kroger Shopping List")
    #print("What would like to eat for the week?")
    grocery_list = input("Please enter your grocery list: ")
    items = [item.strip() 
    for item in grocery_list.split(",") 
        if item.strip()]
    results = search_kroger(items)
    print(results)


if __name__ == '__main__':
    main()
