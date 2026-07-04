import ollama

from src.config import Config


class LLMClient:
    def __init__(self):
        self.client = ollama.Client(host=Config.OLLAMA_HOST)
        self.model = Config.MODEL

    def chat(self, messages, enforce_json=False):
        kwargs = {
            "model": self.model,
            "messages": messages,
            "options": {"temperature": Config.TEMPERATURE},
        }
        if enforce_json:
            kwargs["format"] = "json"
        response = self.client.chat(**kwargs)
        return response["message"]["content"]
