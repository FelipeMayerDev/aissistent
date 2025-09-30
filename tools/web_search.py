from app.tool_manager import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """
    Performs a web search for the given query and returns relevant results.
    Args:
        query: Query string to search for
    Returns:
        A formatted string of search results
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            formatted_results = "\n".join([
                f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}"
                for r in results
            ])
            return formatted_results or "No results found."
    except Exception as e:
        return f"Error performing web search: {str(e)}"