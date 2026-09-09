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
    flight_results: str
    hotel_results: str
    itinerary: str


def flight_agent(state: TravelState):
    return {
        "flight_results": search_flights(state["user_query"])
    }


def hotel_agent(state: TravelState):
    hotels = tavily_search(
        f"best hotels in {state['user_query']}"
    )

    return {
        "hotel_results": hotels
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

graph.add_node("flight", flight_agent)
graph.add_node("hotel", hotel_agent)
graph.add_node("itinerary", itinerary_agent)

graph.add_edge(START, "flight")
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