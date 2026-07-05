import json

class Fato:
    def __init__(self, nome, valores):
        self.nome = nome
        self.valores = valores


class Regra:
    def __init__(self, condicoes, conclusao):
        self.condicoes = condicoes
        self.conclusao = conclusao


class BaseConhecimento:
    def __init__(self):
        self.fatos = []
        self.regras = []

    def adicionar_fato(self, fato):
        self.fatos.append(fato)

    def adicionar_regra(self, regra):
        self.regras.append(regra)

    def remover_regra(self, indice):
        self.regras.pop(indice)

    def salvar(self):
        dados = {
            "fatos": [],
            "regras": []
        }

        for fato in self.fatos:
            dados["fatos"].append({
                "nome": fato.nome,
                "valores": fato.valores
            })

        for regra in self.regras:
            dados["regras"].append({
                "condicoes": regra.condicoes,
                "conclusao": regra.conclusao
            })

        with open("base.json", "w") as f:
            json.dump(dados, f, indent=4)

    def carregar(self):
        self.fatos.clear()
        self.regras.clear()

        with open("base.json", "r") as f:
            dados = json.load(f)

        for f_data in dados["fatos"]:
            self.fatos.append(Fato(f_data["nome"], f_data["valores"]))

        for r_data in dados["regras"]:
            self.regras.append(Regra(r_data["condicoes"], r_data["conclusao"]))


# Backward Chaining 

def provar(objetivo_nome, objetivo_valor, base):
    
    # 1. Verifica se já é fato conhecido
    for fato in base.fatos:
        if fato.nome == objetivo_nome and objetivo_valor in fato.valores:
            return True

    # 2. Procura regras que levam ao objetivo
    for regra in base.regras:

        conclusao_nome, conclusao_valor = regra.conclusao

        if conclusao_nome == objetivo_nome and conclusao_valor == objetivo_valor:

            todas_ok = True

            for condicao_nome, condicao_valor in regra.condicoes:

                if not provar(condicao_nome, condicao_valor, base):
                    todas_ok = False
                    break

            if todas_ok:
                return True

    return False


# Forward Chaining

def forward_chaining(base):

    novos_fatos = True

    while novos_fatos:
        novos_fatos = False

        for regra in base.regras:

            # verifica se regra já foi usada (opcional depois)
            pode_aplicar = True

            for nome, valor in regra.condicoes:

                encontrado = False

                for fato in base.fatos:
                    if fato.nome == nome and valor in fato.valores:
                        encontrado = True
                        break

                if not encontrado:
                    pode_aplicar = False
                    break

            # se todas condições forem verdade
            if pode_aplicar:

                novo_nome, novo_valor = regra.conclusao

                # evita duplicar fato
                existe = False
                for fato in base.fatos:
                    if fato.nome == novo_nome:
                        if novo_valor in fato.valores:
                            existe = True

                if not existe:
                    base.fatos.append(Fato(novo_nome, [novo_valor]))
                    novos_fatos = True