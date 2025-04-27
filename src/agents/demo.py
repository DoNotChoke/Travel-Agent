from llama_index.core.agent.workflow import ReActAgent, ToolCallResult, AgentStream
from llama_index.core import Settings
from src.llm.settings import setting
from src.tools.searching_tools.weather_tool import weather_tool
from src.tools.searching_tools.google_search_tool import google_search_tools
from src.tools.searching_tools.ip_tool import ip_tool
from src.tools.searching_tools.location_tool import location_tool
from src.tools.searching_tools.flight_tool import flight_tool
import asyncio

setting()
agent = ReActAgent(
    name="Weather Agent",
    description="You are a helpful travel guided agent. You are provided different kind of tools to call it and finish"
                "your mission. Consider carefully, thinking before doing.",
    tools=[weather_tool, ip_tool, location_tool, flight_tool] + google_search_tools,
    llm=Settings.llm
)


async def main():
    query = ("I want to go for a holiday in 27/04/2025"
             "Is there any flight from Haneda Airport (Tokyo) to Heathrow Airline in Europe?"
             "Please find the information about the airline, flight schedule and departure airport, arrival airport. "
             "Ensure that the flight_status is active. Ensure to find the iata code for the airport first."
             )
    handler = agent.run(query)

    async for ev in handler.stream_events():
        if isinstance(ev, ToolCallResult):
            print("")
            print("Called tool: ", ev.tool_name, ev.tool_kwargs, "=>", ev.tool_output)
        elif isinstance(ev, AgentStream):  # showing the thought process
            print(ev.delta, end="", flush=True)


if __name__ == "__main__":
    # Chạy event loop async
    asyncio.run(main())
