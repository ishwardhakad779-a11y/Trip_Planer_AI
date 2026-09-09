import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
URL = "https://api.aviationstack.com/v1/flights"


def search_flights(query: str) -> str:

    if not API_KEY:
        return "AVIATIONSTACK_API_KEY is missing."

    # Example: "flights from Delhi to Dubai"
    words = query.lower().split()

    try:
        start = words.index("from") + 1
        end = words.index("to")

        origin = words[start]
        destination = words[end + 1]

    except (ValueError, IndexError):
        return "Please use: flights from Delhi to Dubai"

    airports = {
        "delhi": "DEL",
        "mumbai": "BOM",
        "bangalore": "BLR",
        "kolkata": "CCU",
        "chennai": "MAA",
        "dhaka": "DAC",
        "dubai": "DXB",
        "london": "LHR",
        "paris": "CDG",
        "tokyo": "NRT",
        "newyork": "JFK",
        "singapore": "SIN",
        "bangkok": "BKK",
    }

    origin = airports.get(origin, origin.upper())
    destination = airports.get(destination, destination.upper())

    params = {
        "access_key": API_KEY,
        "dep_iata": origin,
        "arr_iata": destination,
        "limit": 5
    }

    try:
        response = requests.get(URL, params=params, timeout=15)
        data = response.json()

        if "error" in data:
            return f"Flight API error: {data['error'].get('message')}"

        flights = data.get("data", [])

        if not flights:
            return f"No flights found from {origin} to {destination}."

        results = []

        for flight in flights:
            airline = flight.get("airline", {}).get("name", "Unknown")
            number = flight.get("flight", {}).get("iata", "N/A")
            status = flight.get("flight_status", "N/A")

            dep = flight.get("departure", {})
            arr = flight.get("arrival", {})

            results.append(
                f"""
Airline: {airline}
Flight: {number}
Status: {status}
Departure: {dep.get('airport', 'N/A')} ({dep.get('iata', 'N/A')})
Scheduled: {dep.get('scheduled', 'N/A')}
Arrival: {arr.get('airport', 'N/A')} ({arr.get('iata', 'N/A')})
Scheduled: {arr.get('scheduled', 'N/A')}
""".strip()
            )

        return "\n\n---\n\n".join(results)

    except Exception as e:
        return f"Flight search error: {e}"