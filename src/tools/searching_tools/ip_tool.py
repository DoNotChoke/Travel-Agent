from llama_index.core.tools import FunctionTool
from src.tools.api_tool import APIRequest, APIRequestError
import asyncio

base_url = "https://api.ipify.org"
async def get_ip()-> str:
    params = {
        "format": "json"
    }
    try:
        async with APIRequest(base_url) as ip_api_request:
            response = await ip_api_request.api_request(
                endpoint="",
                method="GET",
                params=params
            )

            ip = response.get("ip", "Failed to fetch IP")
            return "Your IP is: {}".format(ip)
    except APIRequestError as e:
        return f"⚠️ IP API Error: {str(e)}"

ip_tool = FunctionTool.from_defaults(
    async_fn=get_ip,
    name="ip_tool",
    description="Calling API to fetch current IP Address."
)