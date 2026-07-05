from knowledge_base import ANIMAIS, ATRIBUTOS
from inference_engine import SessaoInferencia

SEP = "=" * 70


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
                "historico": historico_perguntas,
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
                    "historico": historico_perguntas,
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
                    "historico": historico_perguntas,
                }
            else:
                return {
                    "animal": animal_alvo,
                    "acertou": animal_alvo in sessao.candidatos,
                    "total_perguntas": len(historico_perguntas),
                    "final": "multiplos_candidatos",
                    "historico": historico_perguntas,
                }

        valor_real = ANIMAIS[animal_alvo]["atributos"][pid]
        if random.random() < p_erro:
            resposta = "s" if not valor_real else "n"
        else:
            resposta = "s" if valor_real else "n"

        sessao.aplicar_resposta(pid, resposta)
        historico_perguntas.append((pid, resposta))


import random


def demo_interativo():
    print(SEP)
    print("   DEMONSTRAÇÃO AKINIMAL — Sessões simuladas automáticas")
    print(SEP)

    animais_teste = ["Cachorro", "Golfinho", "Águia", "Polvo", "Elefante", "Pinguim", "Formiga"]

    print(f"\nExecutando {len(animais_teste)} simulações com respostas corretas:\n")

    for animal in animais_teste:
        print("-" * 60)
        print(f"Animal pensado: {animal}")
        resultado = simular_jogada(animal, responder_certo=True)
        status = "✓ ACERTOU" if resultado["acertou"] else "✗ ERROU"
        print(f"  Resultado: {status}")
        print(f"  Perguntas: {resultado['total_perguntas']}")
        print(f"  Modo de fim: {resultado['final']}")

    print("\n" + "=" * 60)
    print("   RESUMO DAS DEMAIS ENTIDADES")
    print("=" * 60)

    total = 0
    acertos = 0
    total_perg = 0
    for nome in ANIMAIS:
        total += 1
        r = simular_jogada(nome, responder_certo=True)
        total_perg += r["total_perguntas"]
        if r["acertou"]:
            acertos += 1

    print(f"  Total de entidades: {total}")
    print(f"  Acertos: {acertos}/{total} ({100*acertos/total:.1f}%)")
    print(f"  Média de perguntas: {total_perg/total:.1f}")
    print()


if __name__ == "__main__":
    demo_interativo()
