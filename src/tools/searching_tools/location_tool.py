from llama_index.core.tools import FunctionTool
import os
from src.tools.api_tool import APIRequest, APIRequestError
from dotenv import load_dotenv
import asyncio


base_url = "http://ip-api.com"


async def get_location(ip_address: str) -> str:
    params = {}
    try:
        async with APIRequest(base_url=base_url) as location_api_request:
            response = await location_api_request.api_request(
                endpoint=f"json/{ip_address}",
                method="GET",
                params=params
            )

            return (
                f"QUERY - {ip_address}\n"
                f"Country: {response['country']}\n"
                f"City: {response['city']}\n"
                f"Latitude: {response['lat']}\n"
                f"Longitude: {response['lon']}\n"
                f"Timezone: {response['timezone']}\n"
            )
    except APIRequestError as e:
        return f"⚠️ Location API Error: {str(e)}"

location_tool = FunctionTool.from_defaults(
    async_fn=get_location,
    name="location_tool",
    description="Fetching API to get information about current location, including: Country, City"
                "Latitude, Longitude, Timezone."
)
