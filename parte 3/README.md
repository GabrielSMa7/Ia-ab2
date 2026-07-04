# AgentIA — Agente de Busca na Internet

Agente que usa **Ollama** + **DuckDuckGo** para pesquisar na internet e responder perguntas com informações atualizadas.

## Pré-requisito: Ollama

Instale o [Ollama](https://ollama.ai) e baixe o modelo:

```bash
ollama pull llama3:8b        # ~4,7 GB
ollama serve                 # manter rodando
```

## Instalação

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python run.py
```

Exemplo de perguntas: `O que é inteligência artificial?`, `Quem é o presidente do Brasil?`, `previsão do tempo`.

## Testes

```bash
pytest tests/ -v
```

## Estrutura

```
parte 3/
├── run.py                  # Entrada principal
├── src/
│   ├── agent.py            # Agente com loop ReAct
│   ├── llm_client.py       # Cliente Ollama
│   ├── tools.py            # web_search (DuckDuckGo)
│   └── config.py           # Configuração
├── tests/
├── docs/relatorio.md       # Relatório técnico
├── requirements.txt
├── pyproject.toml
└── .gitignore
```
