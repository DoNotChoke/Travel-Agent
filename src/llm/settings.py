from llama_index.core import Settings
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv
import os


def setting():
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = TogetherLLM(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        api_key=os.getenv("TOGETHERAI_API_KEY")
    )
