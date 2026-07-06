import json
import os

# ==========================================
# 1. REPRESENTAÇÃO DO CONHECIMENTO
# ==========================================

class Fato:
    def __init__(self, nome, valores):
        self.nome = nome
        self.valores = valores  # Lista de valores possíveis que o fato possui


class Regra:
    def __init__(self, id_regra, condicoes, conclusao, recomendacao=None):
        self.id = f"R{id_regra}"
        self.condicoes = condicoes  # Lista de tuplas [("nome_fato", "valor"), ...]
        self.conclusao = conclusao  # Tupla ("nome_conclusao", "valor")
        self.recomendacao = recomendacao  # Texto opcional com ação/tratamento


class BaseConhecimento:
    def __init__(self):
        self.fatos = []
        self.regras = []
        self.objetivos = []  # Hipóteses principais do domínio

    def adicionar_fato(self, nome, valores):
        # Evita duplicados e mescla valores se o fato já existir
        for fato in self.fatos:
            if fato.nome == nome:
                for v in valores:
                    if v not in fato.valores:
                        fato.valores.append(v)
                return
        self.fatos.append(Fato(nome, valores))

    def adicionar_regra(self, condicoes, conclusao, recomendacao=None):
        id_provisorio = len(self.regras) + 1
        self.regras.append(Regra(id_provisorio, condicoes, conclusao, recomendacao))

    def remover_regra(self, id_regra_str):
        for i, regra in enumerate(self.regras):
            if regra.id == id_regra_str:
                self.regras.pop(i)
                # Reindexa as regras para manter a ordem R1, R2...
                for idx, r in enumerate(self.regras):
                    r.id = f"R{idx + 1}"
                return True
        return False

    def salvar(self, nome_arquivo="base.json"):
        dados = {
            "objetivos": self.objetivos,
            "fatos": [{"nome": f.nome, "valores": f.valores} for f in self.fatos],
            "regras": [
                {
                    "condicoes": r.condicoes,
                    "conclusao": r.conclusao,
                    "recomendacao": r.recomendacao
                } for r in self.regras
            ]
        }
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"[*] Base de conhecimento salva em '{nome_arquivo}' com sucesso!")

    def carregar(self, nome_arquivo="base.json"):
        if not os.path.exists(nome_arquivo):
            return False
        
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
        self.fatos.clear()
        self.regras.clear()
        self.objetivos = dados.get("objetivos", [])

        for f_data in dados.get("fatos", []):
            self.fatos.append(Fato(f_data["nome"], f_data["valores"]))

        for i, r_data in enumerate(dados.get("regras", [])):
            self.regras.append(Regra(i + 1, r_data["condicoes"], r_data["conclusao"], r_data.get("recomendacao")))
        return True


# ==========================================
# 2. MECANISMO DE EXPLICAÇÃO
# ==========================================

class MecanismoExplicacao:
    def __init__(self):
        self.historico_ativacoes = []  # Regras que dispararam e geraram conclusões
        self.objetivo_atual = None     # Qual hipótese está sendo investigada no momento

    def registrar_disparo(self, regra):
        if regra.id not in [item["regra"] for item in self.historico_ativacoes]:
            self.historico_ativacoes.append({
                "regra": regra.id,
                "condicoes": regra.condicoes,
                "conclusao": regra.conclusao,
                "recomendacao": regra.recomendacao
            })

    def explicar_porque(self, fato_perguntado):
        """Justifica por que o sistema está fazendo uma pergunta."""
        if self.objetivo_atual:
            print(f"\n[EXPLICAÇÃO - POR QUÊ?]")
            print(f"-> Estou a perguntar sobre '{fato_perguntado}' porque esta informação")
            print(f"   é necessária para avaliar a hipótese atual: '{self.objetivo_atual}'.")
        else:
            print("\n[-] Nenhuma hipótese específica está sob investigação ativa no momento.")

    def explicar_como(self, nome_diagnostico, valor_diagnostico):
        """Explica passo a passo quais regras geraram o diagnóstico."""
        print(f"\n[EXPLICAÇÃO - COMO?]")
        encontrou = False
        
        for item in self.historico_ativacoes:
            if item["conclusao"][0] == nome_diagnostico and item["conclusao"][1] == valor_diagnostico:
                encontrou = True
                print(f"-> O diagnóstico '{nome_diagnostico} = {valor_diagnostico}' foi deduzido via {item['regra']}.")
                print("   Condições necessárias que foram validadas:")
                for c_nome, c_val in item["condicoes"]:
                    print(f"     - {c_nome} = {c_val}")
                if item["recomendacao"]:
                    print(f"   Tratamento/Ação recomendada: {item['recomendacao']}")
                print("-" * 40)
                
        if not encontrou:
            print(f"-> Não foi encontrada nenhuma regra disparada para '{nome_diagnostico} = {valor_diagnostico}'.")
            print("   Pode ter sido um fato inserido diretamente pelo utilizador.")


# ==========================================
# 3. MOTOR DE INFERÊNCIA
# ==========================================

def backward_chaining(objetivo_nome, objetivo_valor, base, explicacao):
    """Encadeamento para trás puro."""
    # 1. Verifica se já é conhecido na Base de Fatos
    for fato in base.fatos:
        if fato.nome == objetivo_nome:
            if objetivo_valor in fato.valores:
                return True
            else:
                return False  # Já tem outro valor definido, falha a meta

    # 2. Busca regras que concluem o objetivo procurado
    for regra in base.regras:
        conclusao_nome, conclusao_valor = regra.conclusao
        if conclusao_nome == objetivo_nome and conclusao_valor == objetivo_valor:
            
            todas_condicoes_ok = True
            # Tenta provar recursivamente cada pré-condição da regra
            for cond_nome, cond_valor in regra.condicoes:
                if not backward_chaining(cond_nome, cond_valor, base, explicacao):
                    todas_condicoes_ok = False
                    break
            
            if todas_condicoes_ok:
                base.adicionar_fato(objetivo_nome, [objetivo_valor])
                explicacao.registrar_disparo(regra)
                return True

    # 3. Se não há regras nem fatos, pergunta interativamente ao utilizador
    explicacao.objetivo_atual = f"{objetivo_nome} = {objetivo_valor}"
    while True:
        resposta = input(f"O fato '{objetivo_nome}' possui o valor '{objetivo_valor}'? (s/n/por que): ").strip().lower()
        
        if resposta == "por que" or resposta == "porque":
            explicacao.explicar_porque(objetivo_nome)
            continue
        elif resposta == "s":
            base.adicionar_fato(objetivo_nome, [objetivo_valor])
            return True
        elif resposta == "n":
            # Registra que o utilizador negou explicitamente este valor
            return False
        else:
            print("[-] Resposta inválida. Utilize 's', 'n' ou 'por que'.")


def forward_chaining(base, explicacao):
    """Encadeamento para a frente puro. Varre as regras até saturar a base."""
    novos_fatos_inferidos = True
    regras_disparadas = set()

    while novos_fatos_inferidos:
        novos_fatos_inferidos = False

        for regra in base.regras:
            if regra.id in regras_disparadas:
                continue

            pode_aplicar = True
            # Verifica se todas as condições da regra constam nos fatos atuais
            for c_nome, c_valor in regra.condicoes:
                fato_encontrado = False
                for fato in base.fatos:
                    if fato.nome == c_nome and c_valor in fato.valores:
                        fato_encontrado = True
                        break
                if not fato_encontrado:
                    pode_aplicar = False
                    break

            if pode_aplicar:
                c_nome, c_valor = regra.conclusao
                # Verifica se a conclusão já existe
                ja_existe = False
                for fato in base.fatos:
                    if fato.nome == c_nome and c_valor in fato.valores:
                        ja_existe = True
                        break
                
                if not ja_existe:
                    base.adicionar_fato(c_nome, [c_valor])
                    explicacao.registrar_disparo(regra)
                    regras_disparadas.add(regra.id)
                    novos_fatos_inferidos = True


def hybrid_chaining(objetivo_nome, objetivo_valor, base, explicacao):
    """
    ESTRATÉGIA HÍBRIDA (MISTA):
    Usa o Backward Chaining para guiar as perguntas do objetivo. Toda vez que o usuário
    responde 'Sim' adicionando um fato, dispara-se imediatamente o Forward Chaining
    para computar todas as consequências imediatas e evitar perguntas redundantes.
    """
    # 1. Verifica se já é conhecido
    for fato in base.fatos:
        if fato.nome == objetivo_nome:
            return objetivo_valor in fato.valores

    # 2. Busca regras aplicáveis via Backward
    for regra in base.regras:
        conclusao_nome, conclusao_valor = regra.conclusao
        if conclusao_nome == objetivo_nome and conclusao_valor == objetivo_valor:
            todas_condicoes_ok = True
            for cond_nome, cond_valor in regra.condicoes:
                if not hybrid_chaining(cond_nome, cond_valor, base, explicacao):
                    todas_condicoes_ok = False
                    break
            
            if todas_condicoes_ok:
                base.adicionar_fato(objetivo_nome, [objetivo_valor])
                explicacao.registrar_disparo(regra)
                # Dispara forward para propagar a nova conclusão obtida por regra
                forward_chaining(base, explicacao)
                return True

    # 3. Pergunta ao usuário
    explicacao.objetivo_atual = f"{objetivo_nome} = {objetivo_valor}"
    while True:
        resposta = input(f"[HÍBRIDO] O fato '{objetivo_nome}' possui o valor '{objetivo_valor}'? (s/n/por que): ").strip().lower()
        if resposta == "por que" or resposta == "porque":
            explicacao.explicar_porque(objetivo_nome)
            continue
        elif resposta == "s":
            base.adicionar_fato(objetivo_nome, [objetivo_valor])
            # GATILHO HÍBRIDO: Roda o forward imediatamente após a entrada de um fato novo!
            forward_chaining(base, explicacao)
            return True
        elif resposta == "n":
            return False
        else:
            print("[-] Resposta inválida.")


# ==========================================
# 4. INTERFACE INTERATIVA (MENU CLI)
# ==========================================

def menu_editor(base):
    while True:
        print("\n=== MÓDULO EDITOR DA BASE DE CONHECIMENTO ===")
        print("1. Cadastrar Fato Inicial")
        print("2. Cadastrar Nova Regra de Produção")
        print("3. Visualizar Fatos e Regras Atuais")
        print("4. Remover uma Regra")
        print("5. Definir Objetivos/Hipóteses Principais")
        print("6. Salvar Base no Arquivo JSON")
        print("7. Voltar ao Menu Principal")
        
        opcao = input("Selecione uma opção: ").strip()
        
        if opcao == "1":
            nome = input("Nome do Fato (ex: febre): ").strip()
            valores = input("Valores possíveis separados por vírgula (ex: alta, baixa): ").strip().split(",")
            valores = [v.strip() for v in valores]
            base.adicionar_fato(nome, valores)
            print("[+] Fato cadastrado com sucesso!")
            
        elif opcao == "2":
            print("\n--- Cadastro de Regra (SE... ENTÃO...) ---")
            condicoes = []
            while True:
                c_nome = input("Nome do Fato da Condição (ou pressione ENTER para finalizar as condições): ").strip()
                if not c_nome:
                    break
                c_val = input(f"Valor esperado para '{c_nome}': ").strip()
                condicoes.append([c_nome, c_val])
                
            if not condicoes:
                print("[-] Uma regra precisa de pelo menos uma condição.")
                continue
                
            conc_nome = input("Nome do Fato da Conclusão (ex: suspeita): ").strip()
            conc_val = input(f"Valor da Conclusão para '{conc_nome}' (ex: gripe): ").strip()
            recomendacao = input("Recomendação de Ação/Tratamento associada (Opcional - ENTER para pular): ").strip()
            if not recomendacao:
                recomendacao = None
                
            base.adicionar_regra(condicoes, (conc_nome, conc_val), recomendacao)
            print(f"[+] Regra R{len(base.regras)} adicionada com sucesso!")
            
        elif opcao == "3":
            print("\n--- FATOS MAPEADOS ---")
            for f in base.fatos:
                print(f"- {f.nome}: {f.valores}")
            print("\n--- REGRAS CADASTRADAS ---")
            for r in base.regras:
                conds_str = " E ".join([f"({c[0]} = {c[1]})" for c in r.condicoes])
                rec_str = f" [Ação: {r.recomendacao}]" if r.recomendacao else ""
                print(f"- {r.id}: SE {conds_str} ENTÃO ({r.conclusao[0]} = {r.conclusao[1]}){rec_str}")
                
        elif opcao == "4":
            rid = input("Digite o ID da regra a ser removida (ex: R1): ").strip().upper()
            if base.remover_regra(rid):
                print(f"[+] Regra {rid} removida com sucesso e IDs atualizados.")
            else:
                print("[-] Regra não encontrada.")
                
        elif opcao == "5":
            objs = input("Digite os nomes das hipóteses diagnósticas principais separadas por vírgula: ").strip().split(",")
            base.objetivos = [o.strip() for o in objs if o.strip()]
            print("[+] Objetivos definidos!")
            
        elif opcao == "6":
            base.salvar()
            
        elif opcao == "7":
            break


def realizar_diagnostico(base, explicacao):
    if not base.regras:
        print("[-] Erro: A base de conhecimento não possui regras carregadas!")
        return

    print("\n=== MÓDULO CONSULTA E DIAGNÓSTICO ===")
    print("Escolha o método do Motor de Inferência:")
    print("1. Encadeamento para Trás (Backward Chaining)")
    print("2. Encadeamento para a Frente (Forward Chaining)")
    print("3. Encadeamento Misto (Estratégia Híbrida)")
    
    motor = input("Opção: ").strip()
    explicacao.historico_ativacoes.clear() # Limpa histórico anterior

    # Se o utilizador tiver objetivos explícitos mapeados, usa-os
    if base.objetivos:
        print(f"\nHipóteses Alvo Identificadas na Base: {base.objetivos}")
        alvos = []
        for obj_nome in base.objetivos:
            # Coleta quais valores possíveis as regras dão para este objetivo
            for r in base.regras:
                if r.conclusao[0] == obj_nome and r.conclusao[1] not in alvos:
                    alvos.append((obj_nome, r.conclusao[1]))
    else:
        # Se não há objetivos cadastrados, busca as conclusões das últimas regras
        alvos = list(set([r.conclusao for r in base.regras]))

    print(f"Buscando resoluções para os alvos do sistema...")

    diagnostico_encontrado = None

    if motor == "2":
        # Forward pede entradas iniciais e calcula tudo
        print("\n[Forward Chaining] Forneça os Fatos Iniciais Conhecidos:")
        while True:
            nome_f = input("Nome do Fato (ou ENTER para iniciar inferência): ").strip()
            if not nome_f: break
            val_f = input(f"Valor de '{nome_f}': ").strip()
            base.adicionar_fato(nome_f, [val_f])
            
        forward_chaining(base, explicacao)
        
        # Verifica quais alvos foram provados
        print("\n--- RESULTADO DA INFERÊNCIA ---")
        for nome_a, val_a in alvos:
            for fato in base.fatos:
                if fato.nome == nome_a and val_a in fato.valores:
                    print(f"[SUCESSO] Diagnóstico Encontrado: {nome_a} = {val_a}")
                    diagnostico_encontrado = (nome_a, val_a)
                    # Exibe recomendação se houver
                    for item in explicacao.historico_ativacoes:
                        if item["conclusao"] == [nome_a, val_a] and item["recomendacao"]:
                            print(f"[RECOMENDAÇÃO]: {item['recomendacao']}")

    elif motor == "1" or motor == "3":
        # Backward ou Híbrido avaliam hipótese por hipótese perguntando ao usuário
        sucesso = False
        for nome_a, val_a in alvos:
            print(f"\nAvaliar hipótese: {nome_a} = {val_a}...")
            
            if motor == "1":
                resultado = backward_chaining(nome_a, val_a, base, explicacao)
            else:
                resultado = hybrid_chaining(nome_a, val_a, base, explicacao)
                
            if resultado:
                print(f"\n[SUCESSO] Diagnóstico Confirmado: {nome_a} = {val_a}")
                diagnostico_encontrado = (nome_a, val_a)
                
                # Busca recomendação associada no histórico do mecanismo de explicação
                for item in explicacao.historico_ativacoes:
                    if item["conclusao"][0] == nome_a and item["conclusao"][1] == val_a and item["recomendacao"]:
                        print(f"[RECOMENDAÇÃO]: {item['recomendacao']}")
                sucesso = True
                break
        if not sucesso:
            print("\n[-] Nenhuma hipótese pôde ser comprovada com as informações dadas.")

    # Se houve diagnóstico, libera a consulta ao módulo "COMO"
    if diagnostico_encontrado:
        while True:
            resp = input("\nDeseja saber COMO o sistema chegou a esta conclusão? (s/n): ").strip().lower()
            if resp == "s":
                explicacao.explicar_como(diagnostico_encontrado[0], diagnostico_encontrado[1])
                break
            elif resp == "n":
                break


def main():
    base = BaseConhecimento()
    explicacao = MecanismoExplicacao
