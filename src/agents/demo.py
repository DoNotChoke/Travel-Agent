from llama_index.core.agent.workflow import ReActAgent, ToolCallResult, AgentStream
from llama_index.core import Settings
from src.llm.settings import setting
from src.tools.searching_tools.weather_tool import weather_tool
from src.tools.searching_tools.google_search_tool import google_search_tools
import asyncio

setting()
agent = ReActAgent(
    name="Weather Agent",
    description="You are a helpful agent with an ability to call api and retrieve information about weather.",
    tools=[weather_tool] + google_search_tools,
    llm=Settings.llm
)


async def main():
    query = "What the weather look like in Ho Chi Minh City?"
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
