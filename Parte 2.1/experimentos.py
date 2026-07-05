"""
Script de experimentos: executa múltiplas simulações para todas as entidades
da base de conhecimento e coleta métricas de desempenho do sistema.

Métricas coletadas:
  - Número médio de perguntas por sessão
  - Taxa de acerto global
  - Casos de falha por entidade
  - Situações com múltiplas hipóteses ao final

Uso:
    python experimentos.py
"""

import random
from knowledge_base import ANIMAIS, ATRIBUTOS
from inference_engine import SessaoInferencia


def simular_jogada(animal_alvo, responder_certo=True, p_erro=0.0):
    sessao = SessaoInferencia()
    historico_perguntas = []

    while True:
        if sessao.candidatos_restantes() == 0:
            return {
                "animal": animal_alvo,
                "acertou": False,
                "total_perguntas": len(historico_perguntas),
                "final": "sem_candidatos",
                "candidatos_finais": [],
            }

        if sessao.candidatos_restantes() <= 3 and len(sessao.historico) >= 2:
            top = sessao.top_candidatos(3)
            acertou = animal_alvo in top
            if acertou and responder_certo:
                return {
                    "animal": animal_alvo,
                    "acertou": True,
                    "total_perguntas": len(historico_perguntas),
                    "final": "adivinhado",
                    "candidatos_finais": top,
                }
            else:
                for a in top:
                    if a != animal_alvo:
                        sessao.candidatos.discard(a)
                if not acertou and top:
                    sessao.candidatos.discard(top[0])
                continue

        pid = sessao.obter_proxima_pergunta()
        if pid is None or sessao.todas_perguntas_usadas():
            if sessao.candidatos_restantes() == 1:
                animal_final = list(sessao.candidatos)[0]
                return {
                    "animal": animal_alvo,
                    "acertou": animal_final == animal_alvo,
                    "total_perguntas": len(historico_perguntas),
                    "final": "unico_candidato",
                    "candidatos_finais": [animal_final],
                }
            else:
                return {
                    "animal": animal_alvo,
                    "acertou": animal_alvo in sessao.candidatos,
                    "total_perguntas": len(historico_perguntas),
                    "final": "multiplos_candidatos",
                    "candidatos_finais": list(sessao.candidatos),
                }

        valor_real = ANIMAIS[animal_alvo]["atributos"][pid]
        if random.random() < p_erro:
            resposta = "s" if not valor_real else "n"
        else:
            resposta = "s" if valor_real else "n"

        sessao.aplicar_resposta(pid, resposta)
        historico_perguntas.append((pid, resposta))


def main():
    print("=" * 70)
    print("   EXPERIMENTOS — AKINIMAL (Sistema de Identificação de Animais)")
    print("=" * 70)

    todos_animais = list(ANIMAIS.keys())
    total_entidades = len(todos_animais)
    total_atributos = len(ATRIBUTOS)

    print(f"\nResumo da base de conhecimento:")
    print(f"  Entidades: {total_entidades}")
    print(f"  Atributos: {total_atributos}")
    print(f"  Total de células na matriz: {total_entidades * total_atributos}")

    resultados_certos = []
    for animal in todos_animais:
        r = simular_jogada(animal, responder_certo=True)
        resultados_certos.append(r)

    print(f"\n{'='*70}")
    print(f"   RESULTADOS — Respostas 100% corretas")
    print(f"{'='*70}")

    acertos = sum(1 for r in resultados_certos if r["acertou"])
    total_perg = sum(r["total_perguntas"] for r in resultados_certos)
    falhas = [r for r in resultados_certos if not r["acertou"]]
    multi = [r for r in resultados_certos if r["final"] == "multiplos_candidatos"]

    print(f"  Taxa de acerto: {acertos}/{total_entidades} ({100*acertos/total_entidades:.1f}%)")
    print(f"  Média de perguntas por sessão: {total_perg/total_entidades:.2f}")
    print(f"  Sessões com falha: {len(falhas)}")
    print(f"  Sessões com múltiplos candidatos: {len(multi)}")

    if falhas:
        print(f"\n  Casos de falha:")
        for f in falhas:
            print(f"    - {f['animal']}: final={f['final']}, perguntas={f['total_perguntas']}")
            if f["candidatos_finais"]:
                print(f"      candidatos: {', '.join(f['candidatos_finais'])}")

    resultados_erro = []
    for animal in todos_animais:
        r = simular_jogada(animal, responder_certo=True, p_erro=0.3)
        resultados_erro.append(r)

    print(f"\n{'='*70}")
    print(f"   RESULTADOS — 30% de respostas erradas (simulação de erro humano)")
    print(f"{'='*70}")

    acertos2 = sum(1 for r in resultados_erro if r["acertou"])
    total_perg2 = sum(r["total_perguntas"] for r in resultados_erro)
    falhas2 = [r for r in resultados_erro if not r["acertou"]]

    print(f"  Taxa de acerto: {acertos2}/{total_entidades} ({100*acertos2/total_entidades:.1f}%)")
    print(f"  Média de perguntas por sessão: {total_perg2/total_entidades:.2f}")
    print(f"  Sessões com falha: {len(falhas2)}")

    if falhas2:
        print(f"\n  Casos de falha (com 30% de erro):")
        for f in falhas2:
            print(f"    - {f['animal']}: final={f['final']}, perguntas={f['total_perguntas']}")

    print(f"\n{'='*70}")
    print(f"   ANÁLISE POR ENTIDADE (respostas corretas)")
    print(f"{'='*70}")
    print(f"{'Animal':<15} {'Pergs':<7} {'Acertou':<8} {'Final':<22}")
    print("-" * 52)
    for r in sorted(resultados_certos, key=lambda x: x["total_perguntas"]):
        status = "✓" if r["acertou"] else "✗"
        print(f"{r['animal']:<15} {r['total_perguntas']:<7} {status:<8} {r['final']:<22}")

    print(f"\nFim dos experimentos.\n")


if __name__ == "__main__":
    main()
