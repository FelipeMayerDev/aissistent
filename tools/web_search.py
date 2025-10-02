from app.tool_manager import tool
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

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

@tool
def browse_web_page(url: str) -> str:
    """
    Fetches the text content of a web page from a given URL.
    Args:
        url: The URL of the web page to browse.
    Returns:
        The extracted text content of the page, or an error message.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text(separator='\n', strip=True)
        return text_content or "No text content found on the page."
    except Exception as e:
        return f"Error browsing web page: {str(e)}"
        