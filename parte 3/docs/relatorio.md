# Relatório Técnico — AgentIA: Agente de Busca Baseado em LLM

**Disciplina:** Inteligência Artificial
**Ferramentas:** Ollama, DuckDuckGo, Python

---

## 1. Introdução

Agentes baseados em Large Language Models (LLMs) combinam a capacidade de compreensão linguística dos LLMs com ferramentas externas, permitindo respostas factuais e atualizadas. Este projeto implementa o **AgentIA**, um agente que pesquisa na internet via DuckDuckGo e responde perguntas usando o modelo Llama 3 (Ollama).

---

## 2. Arquitetura

### 2.1 Padrão ReAct (Reasoning + Acting)

O agente segue o padrão ReAct (Yao et al., 2022), que intercala raciocínio e ação:

```
1. PERCEBER → recebe a pergunta do usuário
2. PENSAR   → LLM decide se precisa da ferramenta web_search
3. AGIR     → executa web_search(query) no DuckDuckGo
4. OBSERVAR → recebe os resultados da busca
5. ← voltar ao passo 2 (se precisar refinar a busca)
6. RESPONDER → resposta final com base nos resultados
```

### 2.2 Fluxo

```
Pergunta → LLM → precisa pesquisar? → SIM → web_search → DuckDuckGo
                → NÃO → resposta direta (saudações)
                                              ↓
                                    LLM analisa resultados
                                              ↓
                                    Resposta final
```

---

## 3. Tecnologias

| Tecnologia | Finalidade |
|---|---|
| **Ollama** (llama3:8b) | Execução local do LLM, sem API externa |
| **DuckDuckGo Search** | Busca gratuita, sem chave de API |
| **Rich** | Interface colorida no terminal |

### 3.1 Por que Ollama?

O Ollama permite rodar modelos localmente sem depender de serviços pagos ou internet para o processamento das perguntas. Apenas a busca (DuckDuckGo) requer conexão.

---

## 4. Implementação

### 4.1 Agent (`src/agent.py`)

Classe principal com o loop ReAct. O system prompt instrui o LLM a responder em JSON:

```json
// Para pesquisar:
{"tool": "web_search", "args": {"query": "termo de busca"}}

// Para resposta final:
{"answer": "resposta completa baseada nos resultados"}
```

### 4.2 Tools (`src/tools.py`)

Única ferramenta: `web_search(query)` — pesquisa no DuckDuckGo e retorna título, URL e descrição dos top resultados.

### 4.3 LLM Client (`src/llm_client.py`)

Comunicação com a API do Ollama (`http://localhost:11434/api/chat`) usando o parâmetro `format="json"` para garantir saída estruturada.

---

## 5. Exemplo de Execução

```
Pergunta: O que é inteligência artificial?

[LLM] → {"tool": "web_search", "args": {"query": "inteligência artificial definição"}}
[Web]  → Retorna resultados da Wikipedia, IBM, etc.
[LLM]  → {"answer": "Inteligência artificial é um campo da ciência da computação..."}
```

---

## 6. Como Executar

### Pré-requisitos

1. Python 3.10+
2. [Ollama](https://ollama.ai) instalado
3. Modelo baixado: `ollama pull llama3:8b`
4. Ollama rodando: `ollama serve`

### Passos

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Testes

```bash
pytest tests/ -v
```

---

## 7. Conclusão

O AgentIA demonstra o padrão ReAct na prática: um LLM que **raciocina**, **decide** quando buscar informação externa, **executa** a busca e **sintetiza** os resultados. O projeto é auto-contido (apenas Ollama + Python) e não depende de APIs pagas.

---

## 8. Referências

- Yao et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv:2210.03629.
- Ollama. https://ollama.ai
- DuckDuckGo Search. https://pypi.org/project/ddgs/
