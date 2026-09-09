import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def tavily_search(query: str) -> str:
    try:
        results = client.search(
            query=query,
            search_depth="basic",
            max_results=5
        )

        return "\n\n".join(
            f"{r['title']}\n{r['content']}"
            for r in results.get("results", [])
        )

    except Exception as e:
        return f"Search error: {e}"