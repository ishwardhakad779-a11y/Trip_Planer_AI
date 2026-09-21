import os
import sqlite3
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from tools.flight_tool import search_flights
from tools.tavily_tool import tavily_search


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)


class TravelState(TypedDict):
    user_query: str
    destination: str
    flight_results: str
    hotel_results: str
    itinerary: str


# ============================================================
# NEW: Extract clean destination city from user query
# ============================================================

def extract_destination(user_query: str) -> str:
    prompt = f"""
Extract ONLY the destination city/place name from this trip request.
Return just the city name, nothing else. No extra words, no punctuation.

Trip request: "{user_query}"

City:"""

    response = llm.invoke(prompt)
    return response.content.strip()


def destination_agent(state: TravelState):
    return {
        "destination": extract_destination(state["user_query"])
    }


def flight_agent(state: TravelState):
    return {
        "flight_results": search_flights(state["user_query"])
    }


def hotel_agent(state: TravelState):
    # FIX: use clean destination instead of full user_query
    hotels_raw = tavily_search(
        f"best hotels in {state['destination']}"
    )

    # NEW: summarize raw search results into clean short points
    summary_prompt = f"""
Below is raw web search data about hotels in {state['destination']}.
Extract ONLY 3-5 real hotel names with a 1-line description each.
Remove ads, unrelated text, links, and noise.
If no clear hotel names are found, say "No specific hotels found."

Raw data:
{hotels_raw}

Clean hotel list:"""

    cleaned = llm.invoke(summary_prompt)

    return {
        "hotel_results": cleaned.content.strip()
    }


def itinerary_agent(state: TravelState):
    prompt = f"""
Create a short travel itinerary.

Trip:
{state["user_query"]}

Flights:
{state["flight_results"]}

Hotels:
{state["hotel_results"]}

For each day use:

Day 1
Morning:
Afternoon:
Evening:

Day 2
Morning:
Afternoon:
Evening:

Continue according to the trip duration.

Keep activities short.
Do not write long paragraphs.
Do not invent flight, hotel or price information.
"""

    response = llm.invoke(prompt)

    return {
        "itinerary": response.content
    }


graph = StateGraph(TravelState)

graph.add_node("destination", destination_agent)
graph.add_node("flight", flight_agent)
graph.add_node("hotel", hotel_agent)
graph.add_node("itinerary", itinerary_agent)

graph.add_edge(START, "destination")
graph.add_edge("destination", "flight")
graph.add_edge("flight", "hotel")
graph.add_edge("hotel", "itinerary")
graph.add_edge("itinerary", END)


conn = sqlite3.connect(
    "tripmate.db",
    check_same_thread=False
)

memory = SqliteSaver(conn)

travel_graph = graph.compile(
    checkpointer=memory
)


def run_travel_agent(user_input: str, thread_id: str):
    result = travel_graph.invoke(
        {
            "user_query": user_input,
            "destination": "",
            "flight_results": "",
            "hotel_results": "",
            "itinerary": ""
        },
        {
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return {
        "thread_id": thread_id,
        "flight_results": result["flight_results"],
        "hotel_results": result["hotel_results"],
        "itinerary": result["itinerary"]
    }