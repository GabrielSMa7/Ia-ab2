# Sistema de Diagnóstico Médico Baseado em Casos (CBR)

Protótipo educacional de um sistema de apoio ao diagnóstico médico utilizando
a técnica de **Raciocínio Baseado em Casos (Case-Based Reasoning – CBR)**.

> ⚠️ **AVISO**: este sistema tem finalidade **exclusivamente educacional**,
> para estudo da técnica de CBR em Inteligência Artificial. **NÃO** deve ser
> utilizado como ferramenta real de diagnóstico médico. Todos os casos da
> base são fictícios.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `cbr_engine.py` | Núcleo do sistema: representação dos casos, base de conhecimento (20 casos fictícios / 8 doenças), cálculo de similaridade e as 4 etapas do ciclo CBR (Retrieve, Reuse, Revise, Retain). |
| `main.py` | Interface de linha de comando (CLI) interativa para uso manual do sistema. |
| `demo.py` | Script de demonstração automática (não interativo) que executa 5 consultas de exemplo, mostrando passo a passo o ciclo CBR completo. |
| `casos.json` | Base de casos persistida (gerada automaticamente na primeira execução do `main.py`). |

## Como executar

Requer apenas Python 3 (sem bibliotecas externas).

### Modo interativo
```bash
python3 main.py
```
Menu disponível:
1. Diagnosticar novo paciente (ciclo CBR completo: Retrieve → Reuse → Revise → Retain)
2. Listar casos da base de conhecimento
3. Adicionar caso manualmente à base
4. Ver doenças cadastradas
5. Restaurar base de casos padrão
0. Sair

### Modo demonstração (automático)
```bash
python3 demo.py
```
Executa 5 consultas de exemplo cobrindo diferentes doenças da base (Dengue,
Enxaqueca, um caso ambíguo Gripe/COVID-19 corrigido na etapa Revise,
Gastroenterite em criança e Sinusite), exibindo todas as etapas do ciclo CBR.

## Resumo da técnica implementada

- **Representação do caso**: sintomas (conjunto), faixa etária, duração dos
  sintomas em dias (problema) + diagnóstico e tratamento (solução).
- **Similaridade**: combinação ponderada de Coeficiente de Jaccard sobre o
  conjunto de sintomas (peso 0.8) com similaridade local de faixa etária
  (peso 0.1) e duração dos sintomas (peso 0.1).
- **Retrieve**: top-3 casos mais similares acima de um limiar.
- **Reuse**: votação ponderada pela similaridade entre os casos recuperados,
  o tratamento é herdado do caso mais similar com o diagnóstico vencedor.
- **Revise**: validação humana (confirmar ou corrigir diagnóstico/tratamento).
- **Retain**: o caso validado é adicionado e persistido na base (`casos.json`),
  permitindo que o sistema aprenda com a experiência ao longo do tempo.
