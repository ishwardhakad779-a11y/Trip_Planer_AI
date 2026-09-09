# TripMate AI

TripMate AI is an AI-based travel planner built with Python, LangGraph and external APIs.

The user can enter a travel request like:

Plan a 3 day trip from Delhi to Dubai

The application searches for flight information, searches the web for hotel information and generates a day-by-day travel itinerary.

## Features

- Flight search using AviationStack API
- Hotel search using Tavily
- AI itinerary generation using Groq
- LangGraph workflow
- SQLite checkpointing
- FastAPI backend
- Web interface
- Environment variables for API keys

## Project Structure

trip_planer_ai/
│
├── app.py
├── backend.py
├── .env
├── tripmate.db
├── pyproject.toml
├── uv.lock
│
└── tools/
    ├── flight_tool.py
    └── tavily_tool.py

## Workflow

User Request
    ↓
Flight Agent
    ↓
Hotel Agent
    ↓
Itinerary Agent
    ↓
Travel Results

The Flight Agent searches for flight information using AviationStack.

The Hotel Agent searches the web for hotel information using Tavily.

The Itinerary Agent uses the available travel information and Groq LLM to create a day-by-day itinerary.

LangGraph is used to control the workflow and SQLite is used for checkpointing.

## Tech Stack

- Python
- FastAPI
- LangGraph
- LangChain
- Groq
- Tavily
- AviationStack
- SQLite
- Uvicorn
- HTML
- CSS
- JavaScript
- uv

## Installation

### 1. Clone the repository

git clone ishwardhakad779-a11y

cd trip_planer_ai

### 2. Create virtual environment

uv venv

### 3. Activate virtual environment

For Windows PowerShell:

.venv\Scripts\activate

### 4. Install dependencies

uv sync

If you are setting up the project manually, install the required packages:

uv add fastapi uvicorn python-dotenv langchain-groq langgraph langgraph-checkpoint-sqlite

uv add requests certifi airportsdata pycountry

uv add tavily-python

## Environment Variables

Create a `.env` file in the root directory.

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key

Do not upload the `.env` file to GitHub.

Add the following to `.gitignore`:

.env
.venv/
__pycache__/
tripmate.db

## Run the Application

Activate the virtual environment:

.venv\Scripts\activate

Start the application:

uv run python app.py

Open the application in your browser:

http://localhost:8000

## Example

Enter:

Plan a 3 day trip from Delhi to Dubai

The application will:

1. Search for flight information.
2. Search for hotel information.
3. Generate a day-by-day itinerary.
4. Display the results in the web interface.

## API

The application also provides a FastAPI endpoint.

POST /api/travel

Example request:

{
    "message": "Plan a 3 day trip from Delhi to Dubai"
}

The response contains:

- Flight results
- Hotel results
- Generated itinerary
- Thread ID

## Main Files

### app.py

Contains the FastAPI application and the web interface.

### backend.py

Contains the LangGraph workflow, agents, Groq LLM setup and SQLite checkpointing.

### tools/flight_tool.py

Handles flight searches using the AviationStack API.

### tools/tavily_tool.py

Handles web searches using Tavily.

### tripmate.db

SQLite database used for LangGraph checkpointing.

## Why I Built This

I built this project to understand how LangGraph can be used to connect different tasks in an AI application.

The travel planning process is divided into separate steps. Flight search, hotel search and itinerary generation each have their own role, while LangGraph manages the flow between them.

## Future Improvements

- Flight filtering by date and price
- Better hotel result formatting
- Weather information
- Budget-based trip planning
- More travel APIs
- Better conversation history
- User authentication
- Deployment

## Author

Ishwar Dhakad