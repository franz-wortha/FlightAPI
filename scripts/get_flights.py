import requests
import json

url = "http://localhost:1337/api/flights"

payload = {}
headers = {}

response = requests.request(
    "GET",
    url,
    headers=headers,
    data=payload
    )

# Deserialise and Unmarshal JSON for prettier printing
# Define fields to skip
dont_print = ['createdAt', 'publishedAt']

if response.status_code == 200:
    data = response.json()['data']
    print(f"{'ID':<30} | {'AIRLINE NAME'}")
    print("-" * 50)
    for entry in data:
        for k, v in entry.items():
            # Skip unecessary fields
            if k in dont_print:
                continue
            # Print only the first thirty characters
            print(f"{k:<30} | {str(v):<30}")
else:
    print(f"Error: {response.status_code}")