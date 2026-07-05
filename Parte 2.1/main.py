from knowledge_base import ANIMAIS, ATRIBUTOS
from inference_engine import SessaoInferencia


SEP = "=" * 70


def exibir_cabecalho():
    print(SEP)
    print("              AKINIMAL — Adivinhe o Animal!")
    print("     Pense em um animal e eu tentarei descobrir qual é.")
    print(SEP)


def ler_resposta():
    while True:
        r = input("  Resposta (s/n/ns): ").strip().lower()
        if r in ("s", "n", "ns"):
            return r
        print("  Resposta inválida! Digite 's' (Sim), 'n' (Não) ou 'ns' (Não Sei).")


def encerrar_com_sucesso(sessao, animal):
    desc = ANIMAIS[animal]["descricao"]
    print(f"\n  O animal que você pensou é: {animal.upper()}!")
    print(f"  {desc}")
    print(f"  Perguntas feitas: {len(sessao.historico)}")
    return True


def mostrar_hipotese_atual(sessao):
    top = sessao.top_candidatos(3)
    print(f"\n  Hipóteses restantes: {sessao.candidatos_restantes()}")
    if top:
        print(f"  Mais provável: {top[0]}")
        if len(top) > 1:
            print(f"  Alternativas: {', '.join(top[1:])}")


def tentar_adivinhar(sessao):
    top = sessao.top_candidatos(3)
    for animal in top:
        print(f"\n  Meu palpite: é {animal}?")
        desc = ANIMAIS[animal]["descricao"]
        print(f"  ({desc})")
        r = ler_resposta()
        if r == "s":
            encerrar_com_sucesso(sessao, animal)
            return True
        else:
            sessao.candidatos.discard(animal)
            if r == "n":
                print("  OK, descartado!")
            else:
                print("  OK, descartado também!")
    return False


def jogar():
    exibir_cabecalho()
    input("\n  Pressione Enter quando tiver pensado em um animal...")
    print()

    sessao = SessaoInferencia()
    ja_tentou_adivinhar = False

    while True:
        if sessao.candidatos_restantes() == 0:
            print("\n  Não foi possível identificar o animal com as informações fornecidas.")
            print("  Talvez ele não esteja na minha base de conhecimento.")
            break

        if sessao.candidatos_restantes() <= 3 and len(sessao.historico) >= 2:
            if not ja_tentou_adivinhar:
                ja_tentou_adivinhar = True
                if tentar_adivinhar(sessao):
                    return
                continue

        ja_tentou_adivinhar = False

        pid = sessao.obter_proxima_pergunta()
        if pid is None or sessao.todas_perguntas_usadas():
            if sessao.candidatos_restantes() == 1:
                animal = list(sessao.candidatos)[0]
                encerrar_com_sucesso(sessao, animal)
                return
            elif sessao.candidatos_restantes() > 0:
                print("\n  Não há mais perguntas para fazer.")
                print(f"  Candidatos restantes: {', '.join(sessao.candidatos)}")
            break

        pergunta_texto = ATRIBUTOS[pid][1]
        print(f"\n  Pergunta {len(sessao.historico) + 1}: {pergunta_texto}")
        resposta = ler_resposta()
        sessao.aplicar_resposta(pid, resposta)
        mostrar_hipotese_atual(sessao)

    print(f"\n  Fim do jogo. Total de perguntas: {len(sessao.historico)}")


if __name__ == "__main__":
    jogar()
