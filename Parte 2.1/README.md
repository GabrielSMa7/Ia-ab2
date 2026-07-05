# Akinimal — Sistema de Identificação de Animais

Sistema baseado em conhecimento inspirado no Akinator, capaz de identificar
um animal pensado pelo usuário através de perguntas de Sim/Não/Não Sei.

## Como executar

```bash
python3 main.py
```

## Arquivos

| Arquivo | Descrição |
|---|---|
| `main.py` | Interface CLI interativa para jogar |
| `knowledge_base.py` | Base de conhecimento (23 animais, 20 atributos) |
| `inference_engine.py` | Motor de inferência por eliminação de hipóteses |
| `demo.py` | Demonstração automática com simulações |
| `experimentos.py` | Bateria de testes para coletar métricas |
| `relatorio_tecnico.md` | Relatório técnico completo |

## Como jogar

1. Execute `python3 main.py`
2. Pense em um animal
3. Responda as perguntas com `s` (Sim), `n` (Não) ou `ns` (Não Sei)
4. O sistema tentará adivinhar o animal

## Exemplo

```
Pergunta 1: É mamífero? (s/n/ns): s
Hipóteses restantes: 13
Mais provável: Cachorro
```

## Demonstração automática

```bash
python3 demo.py
```

## Experimentos

```bash
python3 experimentos.py
```

## Requisitos

Python 3.6+ (sem bibliotecas externas).
