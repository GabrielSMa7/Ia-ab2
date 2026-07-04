from ddgs import DDGS

from src.config import Config


def web_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=Config.MAX_SEARCH_RESULTS))
            if not results:
                return "Nenhum resultado encontrado."
            formatted = []
            for i, r in enumerate(results, 1):
                formatted.append(
                    f"{i}. {r.get('title', 'Sem título')}\n"
                    f"   URL: {r.get('href', 'Sem link')}\n"
                    f"   {r.get('body', 'Sem descrição')}"
                )
            return "\n\n".join(formatted)
    except Exception as e:
        return f"Erro ao pesquisar: {e}"
