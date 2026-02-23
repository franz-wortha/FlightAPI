# %%
import requests

BASE_URL = "http://localhost:1337/api"

# %%
airlines_data = ["American Airlines", "Delta Air Lines", "Lufthansa", "Emirates", "British Airways"]

# %%
airports_data = [
    {"code": "JFK", "name": "John F. Kennedy", "country": "USA", "state": "NY", "city": "New York"},
    {"code": "LHR", "name": "Heathrow", "country": "UK", "state": "London", "city": "London"},
    {"code": "FRA", "name": "Frankfurt Airport", "country": "Germany", "state": "Hesse", "city": "Frankfurt"},
    {"code": "DXB", "name": "Dubai International", "country": "UAE", "state": "Dubai", "city": "Dubai"},
    {"code": "LAX", "name": "Los Angeles Intl", "country": "USA", "state": "CA", "city": "Los Angeles"}
]

# %%
flights_to_create = [
    {"num": "AA100", "seats": 150, "airline": "American Airlines", "orig": "JFK", "dest": "LHR"},
    {"num": "DL250", "seats": 220, "airline": "Delta Air Lines", "orig": "LAX", "dest": "JFK"},
    {"num": "LH404", "seats": 300, "airline": "Lufthansa", "orig": "FRA", "dest": "DXB"},
    {"num": "EK007", "seats": 450, "airline": "Emirates", "orig": "DXB", "dest": "LHR"},
    {"num": "BA001", "seats": 100, "airline": "British Airways", "orig": "LHR", "dest": "JFK"}
]

# %%
# Dictionary to map airlines and airports to documentIds for FK constraints
id_map = {"airlines": {}, "airports": {}}

def get_or_create(endpoint, filter_field, filter_value, payload):
    # Check if it exists
    res = requests.get(f"{BASE_URL}/{endpoint}?filters[{filter_field}][$eq]={filter_value}")
    data = res.json().get('data', [])
    
    if data:
        print(f"Found existing {endpoint}: {filter_value}")
        return data[0]['documentId']
    
    # Otherwise, create it
    print(f"Creating new {endpoint}: {filter_value}")
    res = requests.post(f"{BASE_URL}/{endpoint}", json={"data": payload})
    if res.status_code == 201:
        return res.json()['data']['documentId']
    else:
        print(f"Error creating {filter_value}: {res.text}")
        return None

# %%
for name in airlines_data:
    doc_id = get_or_create("airlines", "Name", name, {"Name": name})
    if doc_id: id_map["airlines"][name] = doc_id

# %%
# 3. PROCESS AIRPORTS
for ap in airports_data:
    payload = {
        "AirportCode": ap["code"], "AirportName": ap["name"],
        "Country": ap["country"], "State": ap["state"], "City": ap["city"]
    }
    doc_id = get_or_create("airports", "AirportCode", ap["code"], payload)
    if doc_id: id_map["airports"][ap["code"]] = doc_id

# %%
f = flights_to_create[0]
check_flight = requests.get(f"{BASE_URL}/flights?filters[FlightNumber][$eq]={f['num']}")
if check_flight.json().get('data'):
    print(f"Flight {f['num']} already exists. Skipping.")

flight_payload = {
        "data": {
            "FlightNumber": f["num"],
            "Seats": f["seats"],
            "Airline": id_map["airlines"].get(f["airline"]),
            "OriginAirport": id_map["airports"].get(f["orig"]),
            "DestinationAirport": id_map["airports"].get(f["dest"])
        }}
flight_payload

# %%
# 4. PROCESS FLIGHTS
print("\nProcessing Flights...")
for f in flights_to_create:
    # Check if Flight already exists
    check_flight = requests.get(f"{BASE_URL}/flights?filters[FlightNumber][$eq]={f['num']}")
    if check_flight.json().get('data'):
        print(f"Flight {f['num']} already exists. Skipping.")
        continue

    flight_payload = {
        "data": {
            "FlightNumber": f["num"],
            "Airline": id_map["airlines"].get(f["airline"]),
            "Seats": f["seats"],
            "OriginAirport": id_map["airports"].get(f["orig"]),
            "DestinationAirport": id_map["airports"].get(f["dest"])
        }
    }
    res = requests.post(f"{BASE_URL}/flights", json=flight_payload)
    if res.status_code == 201:
        print(f"Successfully created Flight {f['num']}")
    else:
        print(f"Failed to create Flight {f['num']}: {res.text}")


