from llama_index.core.tools import FunctionTool
from src.tools.api_tool import APIRequest, APIRequestError
from dotenv import load_dotenv
import os
from typing import Dict, List
import asyncio
import json

load_dotenv()

base_url = "https://api.aviationstack.com/v1"
access_key = os.getenv("AVIATIONSTACK_API_KEY")


async def get_flight(
        flight_status: str = None,
        dep_iata: str = None,
        arr_iata: str = None,
) -> str:
    params = {
        "access_key": access_key,
        "flight_status": flight_status,
        "dep_iata": dep_iata,
        "arr_iata": arr_iata,
    }

    try:
        async with APIRequest(base_url=base_url) as flight_api_request:
            response = await flight_api_request.api_request(
                endpoint="flights",
                method="GET",
                params=params
            )

            flights_data = []
            for data in response.get("data", []):
                flight_info = {
                    "flight_date": data.get("flight_date"),
                    "departure": {
                        "airport": data.get("departure", {}).get("airport"),
                        "terminal": data.get("departure", {}).get("terminal"),
                        "gate": data.get("departure", {}).get("gate"),
                        "scheduled": data.get("departure", {}).get("scheduled")
                    },
                    "arrival": {
                        "airport": data.get("arrival", {}).get("airport"),
                        "terminal": data.get("arrival", {}).get("terminal"),
                        "gate": data.get("arrival", {}).get("gate"),
                        "scheduled": data.get("arrival", {}).get("scheduled")
                    },
                    "airline": data.get("airline", {}).get("name"),
                    "flight_status": data.get("flight_status"),
                    "flight": {
                        "number": data.get("flight", {}).get("number"),
                        "iata": data.get("flight", {}).get("iata")
                    }
                }
                flights_data.append(flight_info)

            return json.dumps(flights_data, indent=2)

    except APIRequestError as e:
        return json.dumps({"error": f"Flight API Error: {str(e)}"})

flight_tool = FunctionTool.from_defaults(
    async_fn=get_flight,
    name="flight_seeking_tool",
    description="Calling API to retrieve flight information in JSON format. "
                "Parameters: flight_status, dep_iata, arr_iata. "
                "You must ensure to find the information about the dep_iata and arr_iata to call this function."
)
