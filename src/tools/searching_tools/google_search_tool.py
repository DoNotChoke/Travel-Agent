from llama_index.tools.google import GoogleSearchToolSpec
from dotenv import load_dotenv
import os
from llama_index.core.tools.tool_spec.load_and_search import LoadAndSearchToolSpec

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
google_search_engine = os.getenv("GOOGLE_SEARCH_ENGINE")
google_spec = GoogleSearchToolSpec(key=google_api_key, engine=google_search_engine)

load_and_search_spec = LoadAndSearchToolSpec.from_defaults(
    google_spec.to_tool_list()[0]
)

google_search_tools = load_and_search_spec.to_tool_list()
