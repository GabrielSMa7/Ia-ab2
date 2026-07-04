import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    MODEL = os.getenv("LLM_MODEL", "llama3:8b")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
