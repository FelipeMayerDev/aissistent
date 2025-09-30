from decimal import Decimal
import requests
from app.tool_manager import tool

@tool
def get_steam_prices(game_titles_list: list[str]) -> str:
    """
    Gets the current prices for a list of games from Steam.
    Args:
        game_titles_list: List of game titles to get prices for
    Returns:
        A formatted string of game prices
    """
    result = []
    try:
        for game in game_titles_list:
            game_name = game.strip()
            url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&l=portuguese&cc=BR"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
                "Content-Type": "application/json; charset=utf-8"
            }

            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()

            data = resp.json()
            if "items" not in data or not data["items"]:
                return "No games found."

            item = data["items"][0]
            name = item.get("name", "Unknown")
            price = item.get("price", 0)
            if not price:
                result.append(f"{name}: Free to Play")
                continue

            price = Decimal(price['final']) / 100
            result.append(f"{name}: R${price:.2f}")

        return "\n".join(result)

    except Exception as e:
        return f"Error fetching game prices: {str(e)}"