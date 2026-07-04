import json
import re

from src.llm_client import LLMClient
from src.tools import web_search

SYSTEM_PROMPT = """Você é um assistente especializado em pesquisa na internet chamado AgentIA.

FERRAMENTA DISPONÍVEL:
- web_search(query): Pesquisa na internet e retorna resultados atuais.

REGRAS:
1. Use web_search para TODA pergunta que exija informações factuais ou atuais.
2. Após receber o resultado, analise e responda com uma resposta completa em português.
3. Se o resultado não for suficiente, faça uma pesquisa mais específica.
4. NUNCA invente informações. Sempre pesquise quando não tiver certeza.
5. Responda em português brasileiro, de forma clara e educada.

FORMATO DE SAÍDA (SEMPRE EM JSON VÁLIDO):
- Para pesquisar: {"tool": "web_search", "args": {"query": "termo de busca"}}
- Para resposta final: {"answer": "resposta completa aqui"}
"""


class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.tools = {"web_search": web_search}

    def _parse_response(self, text):
        text = text.strip()
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return {"answer": text}

    def ask(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        max_iterations = 10
        for _ in range(max_iterations):
            response = self.llm.chat(self.messages, enforce_json=True)
            self.messages.append({"role": "assistant", "content": response})

            parsed = self._parse_response(response)

            if "answer" in parsed:
                return parsed["answer"]

            if "tool" in parsed:
                tool_name = parsed["tool"]
                args = parsed.get("args", {})

                if tool_name in self.tools:
                    if isinstance(args, dict):
                        result = self.tools[tool_name](**args)
                    else:
                        result = self.tools[tool_name](str(args))
                else:
                    result = f"Ferramenta '{tool_name}' não encontrada."

                self.messages.append({
                    "role": "user",
                    "content": f"Resultado da ferramenta '{tool_name}':\n{result}"
                })
                continue

            return response

        return "Número máximo de iterações atingido."

    def reset(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
