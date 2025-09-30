from app.tool_manager import tool
import requests
import json
import re


@tool
def get_weather(location: str) -> str:
    """
    Gets the current weather for a location.
    Args:
        location: The city or location to get weather for
    Returns:
        Weather information for the location
    """
    try:
        url = f"https://www.climaeradar.com.br/previsao-tempo/{location}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }

        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        html = resp.text


        match = re.search(r'"temperature"\s*:\s*\{[^}]*"celsius"\s*:\s*(-?\d+\.?\d*)', html, re.DOTALL)
        if match:
            print(match.groups())
            temperatura = match.group(1)
            return f"A temperatura em {location} é {temperatura}°C"
        return f"Não foi possível encontrar a temperatura para {location}."

    except Exception as e:
        return f"Erro ao buscar temperatura: {str(e)}"