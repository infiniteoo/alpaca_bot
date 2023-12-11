import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Alpaca API credentials
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading URL
AUTH_TOKEN = os.getenv('AUTH')

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
url = "https://broker-api.sandbox.alpaca.markets/"

headers = {
    "accept": "application/json",
    "authorization": f"Basic {AUTH_TOKEN}"
}

# GET ALL ACCOUNTS
""" modifier = "v1/accounts"
response = requests.get(url + modifier, headers=headers)
print(response.text)
# Check if the request was successful   
if response.status_code == 200:
    # Process the response
    data = response.json()  # This converts the JSON response to a Python dictionary
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}") """

    
# ADD A BANK ACCOUNT (WILL SET TO QUEUED AT FIRST)
# account_id = "9bf0db4b-7b17-486f-a592-bbaf4a72c250"
account_id = os.getenv('ACCOUNT_ID')

""" modifier = f"v1/accounts/{account_id}/ach_relationships"

response = requests.post(url + modifier, headers=headers, json={
  "account_owner_name": "Optimistic Buck",
  "bank_account_type": "CHECKING",
  "bank_account_number": "32131231abc",
  "bank_routing_number": "123103716",
  "nickname": "Bank of America Checking"
})
print(response.text) """


# ADD AN ACCOUNT
# POST TO /v1/accounts
# EXAMPLE REQUEST TO SERVER

modifier = "v1/accounts"
""" 
response = requests.post(url + modifier, headers=headers, json={

  "contact": {
    "email_address": "laughing_torvalds_87139843@example.com",
    "phone_number": "720-555-0823",
    "street_address": [
      "20 N San Mateo Dr"
    ],
    "city": "San Mateo",
    "state": "CA",
    "postal_code": "94401"
  },
  "identity": {
    "given_name": "Laughing",
    "family_name": "Torvalds",
    "date_of_birth": "1970-01-01",
    "tax_id": "666-55-4321",
    "tax_id_type": "USA_SSN",
    "country_of_citizenship": "USA",
    "country_of_birth": "USA",
    "country_of_tax_residence": "USA",
    "funding_source": [
      "employment_income"
    ],
    "visa_type": null,
    "visa_expiration_date": null,
    "date_of_departure_from_usa": null,
    "permanent_resident": null
  },
  "disclosures": {
    "is_control_person": false,
    "is_affiliated_exchange_or_finra": false,
    "is_affiliated_exchange_or_iiroc": false,
    "is_politically_exposed": false,
    "immediate_family_exposed": false,
    "is_discretionary": null
  },
  "agreements": [
    {
      "agreement": "customer_agreement",
      "signed_at": "2023-12-11T22:57:40.039679352Z",
      "ip_address": "127.0.0.1",
      "revision": null
    }
  ],
  "documents": [
    {
      "document_type": "identity_verification",
      "document_sub_type": "passport",
      "content": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigD//2Q==",
      "content_data": null,
      "mime_type": "image/jpeg"
    }
  ],
  "trusted_contact": {
    "given_name": "Jane",
    "family_name": "Doe",
    "email_address": "laughing_torvalds_87139843@example.com"
  },
  "minor_identity": null,
  "entity_id": null,
  "additional_information": "",
  "account_type": "",
  "auto_approve": null,
  "beneficiary": null,
  "trading_configurations": null,
  "currency": null,
  "enabled_assets": null,
  "instant": null,
  "entity_identity": null,
  "entity_contact": null,
  "authorized_individuals": null,
  "ultimate_beneficial_owners": null
})
print(response.text) """

# MAKE A VIRTUAL ACH TRANSFER
# POST 

""" Now that you have an existing ACH relationship between the account and their bank, you can fund the account via ACH using the following endpoint POST /v1/accounts/{account_id}/transfers using the relationship_id we got in the response of the previous section. """

""" modifier = f"v1/accounts/{account_id}/transfers"
response = requests.post(url + modifier, headers=headers, json={
 
  "transfer_type": "ach",
  "relationship_id": "",
  "amount": "1000.00",
  "direction": "INCOMING"
})

print(response.text) """

# MAKING A ORDER
""" The most common use case of Alpaca Broker API is to allow your end users to trade on the stock market. To do so simply pass in to
POST /v1/trading/accounts/{account_id}/orders and again replacing the account_id with  your account_id. """

modifier = f"v1/trading/accounts/{account_id}/orders"

response = requests.post(url + modifier, headers=headers, json=
{
  "symbol": "AAPL",
  "qty": 1,
  "side": "buy",
  "type": "market",
  "time_in_force": "day"
})
print(response.text)