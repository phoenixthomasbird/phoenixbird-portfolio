import urllib.request
import json

def search_web(query: str) -> str:
    """
    Real implementation using DuckDuckGo's free instant answer API.
    For production you'd use Serper, Brave Search, or Tavily.
    """
    encoded = urllib.parse.quote(query)
    url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1"
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
            
        results = []
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        for topic in data.get("RelatedTopics", [])[:3]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(topic["Text"])
        
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search failed: {str(e)}"


def read_url(url: str) -> str:
    """Fetch and return plain text content from a URL"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")
        
        # Strip tags very simply — a real project would use BeautifulSoup
        import re
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:3000]  # Return first 3000 chars
    except Exception as e:
        return f"Could not read URL: {str(e)}"
    


    # This is what the LLM sees — write these descriptions carefully
TOOL_DEFINITIONS = [
    {
        "name": "search_web",
        "description": (
            "Search the web for current information on any topic. "
            "Use this when you need facts, recent events, or data you "
            "don't have. Returns a summary of top results."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A clear, specific search query. "
                        "Example: 'population of Kenya 2024' not just 'Kenya'"
                    )
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_url",
        "description": (
            "Fetch and read the full text content of a specific web page. "
            "Use this after searching, when you need more detail from a "
            "specific source. Requires a full URL starting with https://"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Full URL to fetch. Must start with https://"
                }
            },
            "required": ["url"]
        }
    }
]

# Router — maps tool name to function
def execute_tool(name: str, inputs: dict) -> str:
    if name == "search_web":
        return search_web(inputs["query"])
    elif name == "read_url":
        return read_url(inputs["url"])
    else:
        return f"Unknown tool: {name}"