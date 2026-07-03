"""
Interface de linha de comando (CLI) do Sistema de Diagnóstico Médico
Baseado em Casos (CBR).

Execute com:
    python main.py

AVISO: ferramenta exclusivamente educacional. Não usar para diagnósticos reais.
"""

from cbr_engine import (
    BaseDeCasos, Caso, retrieve, reuse, revise, retain,
    calcular_similaridade,
)

SEPARADOR = "=" * 78


def cabecalho():
    print(SEPARADOR)
    print(" SISTEMA DE DIAGNÓSTICO MÉDICO BASEADO EM CASOS (CBR) — PROTÓTIPO EDUCACIONAL")
    print(" Este sistema NÃO substitui avaliação médica profissional.")
    print(SEPARADOR)


def menu_principal():
    print("\nMenu Principal")
    print("1) Diagnosticar novo paciente (ciclo CBR completo)")
    print("2) Listar casos da base de conhecimento")
    print("3) Adicionar caso manualmente à base (sem passar pelo ciclo CBR)")
    print("4) Ver doenças cadastradas na base")
    print("5) Restaurar base de casos padrão (20 casos fictícios iniciais)")
    print("0) Sair")
    return input("Escolha uma opção: ").strip()


def ler_lista(mensagem: str) -> list:
    bruto = input(mensagem)
    itens = [x.strip().lower().replace(" ", "_") for x in bruto.split(",") if x.strip()]
    return itens


def fluxo_diagnostico(base: BaseDeCasos):
    print("\n--- NOVO ATENDIMENTO ---")
    print("Informe os sintomas separados por vírgula.")
    print("Exemplos de termos usados na base: febre, febre_alta, tosse_seca, coriza,")
    print("dor_de_cabeca, dor_muscular, nausea, vomito, diarreia, dor_de_garganta,")
    print("congestao_nasal, fadiga, perda_de_olfato, dor_de_cabeca_pulsatil, etc.")
    sintomas = ler_lista("Sintomas: ")

    idade = input("Faixa etária (crianca / adulto / idoso) [adulto]: ").strip().lower() or "adulto"
    try:
        duracao = int(input("Há quantos dias os sintomas começaram? [1]: ").strip() or "1")
    except ValueError:
        duracao = 1

    consulta = {"sintomas": sintomas, "idade_faixa": idade, "duracao_dias": duracao}

    # ---------- 1) RETRIEVE ----------
    recuperados = retrieve(base, consulta, top_k=3)
    print("\n[RETRIEVE] Casos mais semelhantes encontrados na base:")
    if not recuperados:
        print("  Nenhum caso semelhante encontrado.")
        return
    for i, r in enumerate(recuperados, start=1):
        c = r.caso
        print(f"  {i}. Caso {c.id} | similaridade={r.similaridade:.2f} | "
              f"diagnóstico histórico: {c.diagnostico}")
        print(f"     sintomas do caso: {', '.join(c.sintomas)}")

    # ---------- 2) REUSE ----------
    diag_sug, trat_sug, confianca, votos = reuse(recuperados)
    print("\n[REUSE] Diagnóstico sugerido com base nos casos recuperados:")
    print(f"  -> Diagnóstico sugerido : {diag_sug}")
    print(f"  -> Tratamento sugerido  : {trat_sug}")
    print(f"  -> Confiança (votação ponderada por similaridade): {confianca*100:.1f}%")
    print(f"  -> Distribuição de votos: {votos}")

    # ---------- 3) REVISE ----------
    print("\n[REVISE] Validação humana da sugestão.")
    resposta = input("  O diagnóstico sugerido está correto? (s/n): ").strip().lower()
    if resposta == "s":
        diag_final, trat_final = revise(diag_sug, trat_sug, confirmado=True)
    else:
        diag_corrigido = input("  Informe o diagnóstico correto: ").strip() or diag_sug
        trat_corrigido = input("  Informe o tratamento recomendado: ").strip() or trat_sug
        diag_final, trat_final = revise(diag_sug, trat_sug, confirmado=False,
                                         diagnostico_corrigido=diag_corrigido,
                                         tratamento_corrigido=trat_corrigido)

    print(f"\n  >> Diagnóstico final: {diag_final}")
    print(f"  >> Tratamento final : {trat_final}")

    # ---------- 4) RETAIN ----------
    reter = input("\n[RETAIN] Deseja reter este caso na base de conhecimento? (s/n): ").strip().lower()
    if reter == "s":
        novo = retain(base, consulta, diag_final, trat_final)
        print(f"  Caso {novo.id} adicionado e salvo na base de conhecimento.")
    else:
        print("  Caso não foi retido na base.")


def listar_casos(base: BaseDeCasos):
    print(f"\n--- BASE DE CASOS ({len(base)} casos) ---")
    for c in base.casos:
        origem = "[INICIAL]" if c.origem == "base_inicial" else "[RETIDO]"
        print(f"{origem} {c.id} | {c.diagnostico} | idade={c.idade_faixa} | "
              f"duração={c.duracao_dias}d | sintomas=({', '.join(c.sintomas)})")
        print(f"          tratamento: {c.tratamento}")


def adicionar_caso_manual(base: BaseDeCasos):
    print("\n--- ADICIONAR CASO MANUALMENTE ---")
    sintomas = ler_lista("Sintomas (separados por vírgula): ")
    idade = input("Faixa etária (crianca/adulto/idoso): ").strip().lower() or "adulto"
    try:
        duracao = int(input("Duração dos sintomas em dias: ").strip() or "1")
    except ValueError:
        duracao = 1
    diagnostico = input("Diagnóstico: ").strip()
    tratamento = input("Tratamento recomendado: ").strip()

    import uuid
    novo = Caso(
        id=f"M-{uuid.uuid4().hex[:8]}",
        sintomas=sintomas,
        idade_faixa=idade,
        duracao_dias=duracao,
        diagnostico=diagnostico,
        tratamento=tratamento,
        eficaz=True,
        origem="retido",
    )
    base.casos.append(novo)
    base.salvar()
    print(f"Caso {novo.id} adicionado com sucesso.")


def main():
    cabecalho()
    base = BaseDeCasos("casos.json")
    print(f"Base de conhecimento carregada com {len(base)} casos "
          f"({len(base.listar_doencas())} doenças distintas).")

    while True:
        opcao = menu_principal()
        if opcao == "1":
            fluxo_diagnostico(base)
        elif opcao == "2":
            listar_casos(base)
        elif opcao == "3":
            adicionar_caso_manual(base)
        elif opcao == "4":
            print("\nDoenças cadastradas na base:")
            for d in base.listar_doencas():
                print(f"  - {d}")
        elif opcao == "5":
            confirmar = input("Isso apaga casos retidos manualmente. Confirmar? (s/n): ").strip().lower()
            if confirmar == "s":
                base.reiniciar_base_padrao()
                print("Base restaurada para os 20 casos fictícios iniciais.")
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
