from knowledge_base import ANIMAIS, ATRIBUTOS


class SessaoInferencia:
    def __init__(self):
        self.candidatos = set(ANIMAIS.keys())
        self.perguntas_feitas = set()
        self.historico = []
        self._perguntas_restantes = {id_ for id_, _ in ATRIBUTOS}

    def candidatos_restantes(self):
        return len(self.candidatos)

    def obter_proxima_pergunta(self):
        if not self._perguntas_restantes:
            return None
        melhor_id = None
        melhor_score = -1
        for pid in self._perguntas_restantes:
            sim = 0
            nao = 0
            for nome in self.candidatos:
                if ANIMAIS[nome]["atributos"][pid]:
                    sim += 1
                else:
                    nao += 1
            if sim == 0 or nao == 0:
                continue
            score = min(sim, nao)
            if score > melhor_score:
                melhor_score = score
                melhor_id = pid
        if melhor_id is None:
            for pid in self._perguntas_restantes:
                return pid
        return melhor_id

    def aplicar_resposta(self, id_pergunta, resposta):
        self.perguntas_feitas.add(id_pergunta)
        self._perguntas_restantes.discard(id_pergunta)
        if resposta == "s":
            self.candidatos = {
                nome for nome in self.candidatos
                if ANIMAIS[nome]["atributos"][id_pergunta] is True
            }
        elif resposta == "n":
            self.candidatos = {
                nome for nome in self.candidatos
                if ANIMAIS[nome]["atributos"][id_pergunta] is False
            }
        self.historico.append((id_pergunta, resposta))

    def hipotese_mais_provavel(self):
        if not self.candidatos:
            return None
        return max(self.candidatos, key=lambda nome: self._calcular_peso(nome))

    def _calcular_peso(self, nome):
        peso = 0.0
        animal = ANIMAIS[nome]
        for pid, resposta in self.historico:
            if resposta == "ns":
                continue
            valor_real = animal["atributos"][pid]
            esperado = resposta == "s"
            if valor_real == esperado:
                peso += 1.0
        return peso

    def top_candidatos(self, k=3):
        return sorted(
            self.candidatos,
            key=lambda nome: self._calcular_peso(nome),
            reverse=True,
        )[:k]

    def todas_perguntas_usadas(self):
        return len(self._perguntas_restantes) == 0
