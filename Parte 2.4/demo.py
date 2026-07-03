# -*- coding: utf-8 -*-
"""
Script de demonstração automática (não-interativo) do Sistema de
Diagnóstico Médico Baseado em Casos (CBR).

Executa várias consultas de exemplo cobrindo diferentes doenças da base,
mostrando passo a passo as 4 etapas do ciclo CBR (Retrieve, Reuse, Revise,
Retain). Útil para:
  - validar o funcionamento do sistema sem necessidade de digitação manual;
  - gerar os exemplos de consulta usados no relatório técnico;
  - servir de roteiro para a gravação do vídeo de demonstração.

Execute com:
    python demo.py
"""

import os
import shutil

from cbr_engine import BaseDeCasos, retrieve, reuse, revise, retain

SEP = "-" * 78


def imprimir_caso_recuperado(idx, r):
    c = r.caso
    print(f"   {idx}. Caso {c.id}  (similaridade = {r.similaridade:.3f})")
    print(f"      Diagnóstico histórico: {c.diagnostico}")
    print(f"      Sintomas do caso     : {', '.join(c.sintomas)}")
    print(f"      Idade/Duração        : {c.idade_faixa} / {c.duracao_dias} dia(s)")


def rodar_consulta(base: BaseDeCasos, titulo: str, consulta: dict,
                    aceitar: bool, diag_corrigido=None, trat_corrigido=None):
    print(SEP)
    print(f"CONSULTA: {titulo}")
    print(SEP)
    print(f"Entrada do paciente -> sintomas: {consulta['sintomas']}")
    print(f"                       idade_faixa: {consulta['idade_faixa']} | "
          f"duracao_dias: {consulta['duracao_dias']}")

    # 1) RETRIEVE
    recuperados = retrieve(base, consulta, top_k=3)
    print("\n[1] RETRIEVE - casos mais semelhantes recuperados:")
    for i, r in enumerate(recuperados, start=1):
        imprimir_caso_recuperado(i, r)

    # 2) REUSE
    diag_sug, trat_sug, confianca, votos = reuse(recuperados)
    print("\n[2] REUSE - diagnóstico proposto a partir dos casos recuperados:")
    print(f"    Diagnóstico sugerido : {diag_sug}")
    print(f"    Tratamento sugerido  : {trat_sug}")
    print(f"    Confiança da sugestão: {confianca*100:.1f}%   (votos: {votos})")

    # 3) REVISE
    print("\n[3] REVISE - validação humana:")
    if aceitar:
        diag_final, trat_final = revise(diag_sug, trat_sug, confirmado=True)
        print("    Sugestão CONFIRMADA pelo avaliador.")
    else:
        diag_final, trat_final = revise(diag_sug, trat_sug, confirmado=False,
                                         diagnostico_corrigido=diag_corrigido,
                                         tratamento_corrigido=trat_corrigido)
        print(f"    Sugestão CORRIGIDA pelo avaliador para: {diag_final}")
    print(f"    Diagnóstico final: {diag_final}")
    print(f"    Tratamento final : {trat_final}")

    # 4) RETAIN
    novo = retain(base, consulta, diag_final, trat_final)
    print(f"\n[4] RETAIN - novo caso {novo.id} adicionado e salvo na base "
          f"(total agora: {len(base)} casos).")
    print()
    return {
        "titulo": titulo, "recuperados": recuperados, "diag_sug": diag_sug,
        "confianca": confianca, "diag_final": diag_final, "caso_id": novo.id
    }


def main():
    # usa uma base separada (copia da base "oficial" se existir, senão gera a padrão)
    caminho_demo = "casos_demo.json"
    if os.path.exists(caminho_demo):
        os.remove(caminho_demo)
    base = BaseDeCasos(caminho_demo)

    print("=" * 78)
    print(" DEMONSTRAÇÃO AUTOMÁTICA - SISTEMA DE DIAGNÓSTICO MÉDICO BASEADO EM CASOS")
    print("=" * 78)
    print(f"Base de conhecimento inicial: {len(base)} casos, "
          f"{len(base.listar_doencas())} doenças distintas: {base.listar_doencas()}\n")

    resultados = []

    # Consulta 1: caso muito próximo de um caso de Dengue -> sugestão aceita
    resultados.append(rodar_consulta(
        base, "Paciente adulto com suspeita de Dengue",
        {"sintomas": ["febre_alta", "dor_atras_dos_olhos", "dor_muscular",
                      "manchas_vermelhas_na_pele"],
         "idade_faixa": "adulto", "duracao_dias": 3},
        aceitar=True))

    # Consulta 2: sintomas de Enxaqueca -> sugestão aceita
    resultados.append(rodar_consulta(
        base, "Paciente adulto com dor de cabeça pulsátil",
        {"sintomas": ["dor_de_cabeca_pulsatil", "nausea", "sensibilidade_a_luz"],
         "idade_faixa": "adulto", "duracao_dias": 1},
        aceitar=True))

    # Consulta 3: sintomas ambíguos entre Gripe e COVID-19 -> avaliador corrige
    resultados.append(rodar_consulta(
        base, "Paciente adulto com febre, tosse seca e fadiga (caso ambíguo)",
        {"sintomas": ["febre", "tosse_seca", "fadiga", "dor_muscular"],
         "idade_faixa": "adulto", "duracao_dias": 2},
        aceitar=False, diag_corrigido="COVID-19",
        trat_corrigido="Isolamento, teste confirmatório e monitoramento de saturação de O2."))

    # Consulta 4: criança com sintomas de gastroenterite
    resultados.append(rodar_consulta(
        base, "Criança com diarreia e vômito",
        {"sintomas": ["diarreia", "vomito", "dor_abdominal"],
         "idade_faixa": "crianca", "duracao_dias": 1},
        aceitar=True))

    # Consulta 5: caso novo, sem correspondência forte -> baixa similaridade (sinusite)
    resultados.append(rodar_consulta(
        base, "Paciente adulto com dor facial e congestão prolongada",
        {"sintomas": ["dor_facial", "congestao_nasal", "coriza_espessa"],
         "idade_faixa": "adulto", "duracao_dias": 6},
        aceitar=True))

    # Resumo final
    print("=" * 78)
    print(" RESUMO DAS CONSULTAS EXECUTADAS")
    print("=" * 78)
    for r in resultados:
        top1 = r["recuperados"][0]
        print(f"- {r['titulo']}")
        print(f"  caso mais próximo: {top1.caso.id} (sim={top1.similaridade:.2f}) "
              f"-> diagnóstico final: {r['diag_final']} "
              f"(confiança da sugestão original: {r['confianca']*100:.1f}%) "
              f"-> retido como {r['caso_id']}")
    print(f"\nBase final possui {len(base)} casos "
          f"({len(base.listar_doencas())} doenças distintas).")


if __name__ == "__main__":
    main()
