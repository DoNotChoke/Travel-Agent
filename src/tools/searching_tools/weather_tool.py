import os
from dotenv import load_dotenv
from src.tools.api_tool import APIRequest, APIRequestError
from llama_index.core.tools import FunctionTool

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")
base_url = "https://api.openweathermap.org/data/2.5"


async def get_weather(latitude: float, longitude: float) -> str:
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric"
    }

    try:
        async with APIRequest(base_url=base_url, api_key=api_key) as weather_api_request:
            response = await weather_api_request.api_request(
                endpoint="weather",
                method="GET",
                params=params
            )

            location = response.get("name", "Unknown location")
            return (
                f"🌦️ WEATHER INFORMATION - {location}\n"
                f"🌡️ Temperature: {response['main']['temp']}°C\n"
                f"🌬️ Feels like: {response['main']['feels_like']}°C\n"
                f"☁️ Condition: {response['weather'][0]['description'].capitalize()}\n"
                f"💧 Humidity: {response['main']['humidity']}%\n"
                f"🍃 Wind: {response['wind']['speed']} m/s"
            )

    except APIRequestError as e:
        return f"⚠️ Weather API Error: {str(e)}"

weather_tool = FunctionTool.from_defaults(
    async_fn=get_weather,
    name="weather_tool",
    description="Calling API to retrieve information about the weather in the given coordinates."
)
