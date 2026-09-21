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
        # NOTE: AviationStack free tier does not support filtering by
        # a future date, so results are real-time/live flights only.
        "limit": 3
    }

    try:
        response = requests.get(URL, params=params, timeout=15)
        data = response.json()

        if "error" in data:
            return f"Flight API error: {data['error'].get('message')}"

        flights = data.get("data", [])

        if not flights:
            return f"No live flights found from {origin} to {destination}."

        results = []

        for flight in flights:
            airline = flight.get("airline", {}).get("name", "Unknown")
            number = flight.get("flight", {}).get("iata", "N/A")

            dep = flight.get("departure", {})
            arr = flight.get("arrival", {})

            # FIX: only keep the essentials, drop status/raw timestamps noise
            dep_time = (dep.get("scheduled") or "N/A")[:16].replace("T", " ")
            arr_time = (arr.get("scheduled") or "N/A")[:16].replace("T", " ")

            results.append(
                f"{airline} {number} | {dep.get('iata', 'N/A')} {dep_time} "
                f"-> {arr.get('iata', 'N/A')} {arr_time}"
            )

        note = (
            "(Live flight data — actual flights on your travel date may differ)\n\n"
        )

        return note + "\n".join(results)

    except Exception as e:
        return f"Flight search error: {e}"