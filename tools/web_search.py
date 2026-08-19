import os
from tavily import TavilyClient

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def search_web(query: str):
    try:
        results = client.search(query, max_results=3)
        summaries = [f"{r['title']}: {r['content'][:200]}" for r in results['results']]
        return "\n".join(summaries)
    except Exception as e:
        return f"Error searching the web: {e}"

web_search_schema = {
    "type":"function",
    "function": {
        "name": "web_search",
        "description": "Performs a search on the web with top 3 results, returns a summary",
        "parameters":{
            "type":"object",
            "properties":{
                "query":{
                    "type":"string",
                    "description":"The search query"
                },
            },
            "required":["filepath"]
        }
    }
}