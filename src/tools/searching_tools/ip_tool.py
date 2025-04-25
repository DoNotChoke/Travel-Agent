from llama_index.core.tools import FunctionTool
from src.tools.api_tool import APIRequest

async def get_ip()-> str:
    params = {
        "format": "json"
    }

