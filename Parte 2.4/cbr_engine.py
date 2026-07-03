"""
Sistema de Diagnóstico Médico Baseado em Casos (Case-Based Reasoning - CBR)
============================================================================

Protótipo educacional que implementa o ciclo clássico de Raciocínio Baseado
em Casos (Aamodt & Plaza, 1994):

    1. RETRIEVE  -> localizar os casos mais semelhantes na base de casos
    2. REUSE     -> reaproveitar o(s) caso(s) recuperado(s) para sugerir
                    um diagnóstico e tratamento
    3. REVISE    -> permitir que o usuário (profissional/operador) valide
                    ou corrija a sugestão antes de confirmá-la
    4. RETAIN    -> armazenar o novo caso (já validado) na base, para que
                    o sistema "aprenda" com a experiência

AVISO IMPORTANTE
-----------------
Este sistema tem finalidade EXCLUSIVAMENTE EDUCACIONAL, para fins de estudo
da técnica de Raciocínio Baseado em Casos em Inteligência Artificial.
NÃO deve ser utilizado, em nenhuma hipótese, como ferramenta real de
diagnóstico médico. Os casos contidos na base são fictícios.
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional


# --------------------------------------------------------------------------- #
# 1. REPRESENTAÇÃO DO CASO
# --------------------------------------------------------------------------- #

@dataclass
class Caso:
    """Representa um caso médico na base de conhecimento.

    Um caso em CBR é tradicionalmente dividido em:
      - Problema  (sintomas observados + atributos do paciente)
      - Solução   (diagnóstico + tratamento recomendado)
      - Resultado (desfecho, opcional - aqui usamos 'eficaz' como indicador
                    de que o tratamento funcionou no caso histórico)
    """
    id: str
    sintomas: List[str]                 # PROBLEMA
    idade_faixa: str                    # PROBLEMA (atributo contextual): "crianca", "adulto", "idoso"
    duracao_dias: int                   # PROBLEMA (atributo contextual): há quantos dias os sintomas começaram
    diagnostico: str                    # SOLUÇÃO
    tratamento: str                     # SOLUÇÃO
    eficaz: bool = True                 # RESULTADO
    origem: str = "base_inicial"        # metadado: 'base_inicial' ou 'retido' (novo caso retido)

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict) -> "Caso":
        return Caso(**d)


# --------------------------------------------------------------------------- #
# 2. BASE DE CASOS INICIAL (>= 15 casos, >= 5 doenças distintas)
# --------------------------------------------------------------------------- #
# Vocabulário controlado de sintomas (importante para o cálculo de
# similaridade baseado em conjuntos): todos os casos usam os mesmos termos.

BASE_INICIAL: List[Caso] = [
    # ---------------- GRIPE (Influenza) ----------------
    Caso("C01", ["febre", "calafrios", "dor_de_cabeca", "dor_muscular", "tosse_seca", "fadiga"],
         "adulto", 2, "Gripe (Influenza)",
         "Repouso, hidratação abundante, antitérmico (paracetamol) e isolamento por 5 dias."),
    Caso("C02", ["febre_alta", "calafrios", "dor_muscular", "fadiga", "dor_de_cabeca"],
         "idoso", 1, "Gripe (Influenza)",
         "Repouso, hidratação, antitérmico e avaliação médica por grupo de risco."),
    Caso("C03", ["tosse_seca", "dor_de_garganta", "febre", "dor_muscular", "fadiga"],
         "adulto", 3, "Gripe (Influenza)",
         "Repouso, hidratação, antitérmico e monitoramento de sintomas respiratórios."),

    # ---------------- RESFRIADO COMUM ----------------
    Caso("C04", ["coriza", "espirros", "dor_de_garganta", "tosse_leve", "congestao_nasal"],
         "adulto", 2, "Resfriado Comum",
         "Repouso, hidratação, soro fisiológico nasal e analgésico se necessário."),
    Caso("C05", ["coriza", "espirros", "congestao_nasal", "dor_de_cabeca_leve"],
         "crianca", 1, "Resfriado Comum",
         "Hidratação, lavagem nasal com soro fisiológico e observação."),
    Caso("C06", ["espirros", "congestao_nasal", "tosse_leve", "mal_estar_leve"],
         "adulto", 3, "Resfriado Comum",
         "Repouso, hidratação e descongestionante nasal de venda livre."),

    # ---------------- DENGUE ----------------
    Caso("C07", ["febre_alta", "dor_atras_dos_olhos", "dor_muscular", "manchas_vermelhas_na_pele", "fadiga"],
         "adulto", 3, "Dengue",
         "Hidratação oral intensa, paracetamol (evitar AAS/AINEs) e monitoramento de sinais de alarme."),
    Caso("C08", ["febre_alta", "dor_muscular", "dor_atras_dos_olhos", "nausea", "manchas_vermelhas_na_pele"],
         "adulto", 4, "Dengue",
         "Hidratação oral intensa, repouso e acompanhamento médico para sinais de alarme."),
    Caso("C09", ["febre_alta", "dor_muscular", "nausea", "vomito", "manchas_vermelhas_na_pele"],
         "idoso", 2, "Dengue",
         "Internação para hidratação venosa e monitoramento, dado o grupo de risco."),

    # ---------------- COVID-19 ----------------
    Caso("C10", ["febre", "tosse_seca", "perda_de_olfato", "perda_de_paladar", "fadiga"],
         "adulto", 2, "COVID-19",
         "Isolamento, hidratação, antitérmico e monitoramento de saturação de oxigênio."),
    Caso("C11", ["tosse_seca", "fadiga", "dor_de_garganta", "perda_de_olfato", "dor_de_cabeca"],
         "adulto", 4, "COVID-19",
         "Isolamento, repouso, hidratação e teste confirmatório."),
    Caso("C12", ["febre", "falta_de_ar", "tosse_seca", "fadiga", "dor_muscular"],
         "idoso", 3, "COVID-19",
         "Avaliação médica imediata por falta de ar, monitoramento de saturação de O2."),

    # ---------------- ENXAQUECA (Migrânea) ----------------
    Caso("C13", ["dor_de_cabeca_pulsatil", "nausea", "sensibilidade_a_luz", "sensibilidade_a_som"],
         "adulto", 1, "Enxaqueca",
         "Repouso em ambiente escuro e silencioso, analgésico específico e hidratação."),
    Caso("C14", ["dor_de_cabeca_pulsatil", "nausea", "sensibilidade_a_luz", "vomito"],
         "adulto", 1, "Enxaqueca",
         "Analgésico/antiemético, repouso em ambiente escuro e identificação de gatilhos."),
    Caso("C15", ["dor_de_cabeca_pulsatil", "sensibilidade_a_som", "sensibilidade_a_luz", "fadiga"],
         "adulto", 2, "Enxaqueca",
         "Repouso, analgésico específico e avaliação neurológica se recorrente."),

    # ---------------- GASTROENTERITE ----------------
    Caso("C16", ["diarreia", "nausea", "vomito", "dor_abdominal", "febre"],
         "adulto", 2, "Gastroenterite",
         "Hidratação oral com soro de reidratação, dieta leve e repouso."),
    Caso("C17", ["diarreia", "dor_abdominal", "vomito", "mal_estar_leve"],
         "crianca", 1, "Gastroenterite",
         "Soro de reidratação oral, dieta leve e observação de sinais de desidratação."),

    # ---------------- SINUSITE ----------------
    Caso("C18", ["congestao_nasal", "dor_facial", "dor_de_cabeca", "coriza_espessa", "febre_leve"],
         "adulto", 5, "Sinusite",
         "Lavagem nasal, analgésico e avaliação médica para possível antibiótico se persistir."),
    Caso("C19", ["dor_facial", "congestao_nasal", "tosse_leve", "coriza_espessa"],
         "adulto", 6, "Sinusite",
         "Lavagem nasal com soro fisiológico, analgésico e acompanhamento clínico."),

    # ---------------- FARINGOAMIGDALITE ----------------
    Caso("C20", ["dor_de_garganta", "febre", "dificuldade_para_engolir", "ganglios_inchados"],
         "crianca", 2, "Faringoamigdalite",
         "Analgésico, hidratação e avaliação médica para investigar origem bacteriana."),
]


# --------------------------------------------------------------------------- #
# 3. CÁLCULO DE SIMILARIDADE
# --------------------------------------------------------------------------- #
# Similaridade local para sintomas: Coeficiente de Jaccard sobre o conjunto
# de sintomas (problema "rico em atributos do tipo conjunto").
#
#       sim_sintomas(A, B) = |A ∩ B| / |A ∪ B|
#
# Similaridade local para atributos contextuais (idade e duração) também são
# combinadas, formando uma similaridade global ponderada:
#
#       sim_global = w1 * sim_sintomas + w2 * sim_idade + w3 * sim_duracao
#
# Pesos sugeridos (sintomas têm peso muito maior, pois são o atributo mais
# discriminante para o diagnóstico):
PESO_SINTOMAS = 0.8
PESO_IDADE = 0.1
PESO_DURACAO = 0.1


def similaridade_jaccard(conjunto_a: List[str], conjunto_b: List[str]) -> float:
    """Similaridade de Jaccard entre dois conjuntos de sintomas."""
    a, b = set(conjunto_a), set(conjunto_b)
    if not a and not b:
        return 1.0
    intersecao = len(a & b)
    uniao = len(a | b)
    return intersecao / uniao if uniao else 0.0


def similaridade_idade(idade_a: str, idade_b: str) -> float:
    """Similaridade local simples (1.0 se igual, 0.0 caso contrário)."""
    return 1.0 if idade_a == idade_b else 0.0


def similaridade_duracao(dur_a: int, dur_b: int, escala_max: int = 10) -> float:
    """Similaridade local baseada na diferença normalizada de dias de sintoma."""
    diferenca = abs(dur_a - dur_b)
    return max(0.0, 1.0 - diferenca / escala_max)


def calcular_similaridade(consulta: Dict, caso: Caso) -> float:
    """Similaridade global ponderada entre uma consulta (novo problema) e um caso da base."""
    sim_s = similaridade_jaccard(consulta.get("sintomas", []), caso.sintomas)
    sim_i = similaridade_idade(consulta.get("idade_faixa", ""), caso.idade_faixa)
    sim_d = similaridade_duracao(consulta.get("duracao_dias", 0), caso.duracao_dias)
    return PESO_SINTOMAS * sim_s + PESO_IDADE * sim_i + PESO_DURACAO * sim_d


# --------------------------------------------------------------------------- #
# 4. BASE DE CASOS (com persistência em JSON)
# --------------------------------------------------------------------------- #

class BaseDeCasos:
    def __init__(self, caminho_arquivo: str = "casos.json"):
        self.caminho_arquivo = caminho_arquivo
        self.casos: List[Caso] = []
        self._carregar()

    def _carregar(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            self.casos = [Caso.from_dict(d) for d in dados]
        else:
            self.casos = list(BASE_INICIAL)
            self.salvar()

    def salvar(self):
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.casos], f, ensure_ascii=False, indent=2)

    def reiniciar_base_padrao(self):
        """Restaura a base para os 20 casos fictícios iniciais."""
        self.casos = list(BASE_INICIAL)
        self.salvar()

    def listar_doencas(self) -> List[str]:
        return sorted(set(c.diagnostico for c in self.casos))

    def __len__(self):
        return len(self.casos)


# --------------------------------------------------------------------------- #
# 5. CICLO CBR: RETRIEVE -> REUSE -> REVISE -> RETAIN
# --------------------------------------------------------------------------- #

@dataclass
class ResultadoRecuperacao:
    caso: Caso
    similaridade: float


def retrieve(base: BaseDeCasos, consulta: Dict, top_k: int = 3,
             limiar_minimo: float = 0.0) -> List[ResultadoRecuperacao]:
    """
    ETAPA 1 - RETRIEVE
    Calcula a similaridade da consulta contra todos os casos da base e
    retorna os top_k mais semelhantes (ordenados de forma decrescente),
    descartando os que ficarem abaixo do limiar mínimo.
    """
    resultados = []
    for caso in base.casos:
        sim = calcular_similaridade(consulta, caso)
        if sim >= limiar_minimo:
            resultados.append(ResultadoRecuperacao(caso, sim))
    resultados.sort(key=lambda r: r.similaridade, reverse=True)
    return resultados[:top_k]


def reuse(recuperados: List[ResultadoRecuperacao]) -> Tuple[Optional[str], Optional[str], float, Dict[str, float]]:
    """
    ETAPA 2 - REUSE
    Reaproveita os casos recuperados para sugerir um diagnóstico.
    Estratégia: votação ponderada pela similaridade entre os top_k casos
    recuperados (e não apenas o vizinho mais próximo), tornando a sugestão
    mais robusta a ruído/empates.
    O tratamento sugerido é herdado do caso mais similar dentre os que têm
    o diagnóstico vencedor.
    """
    if not recuperados:
        return None, None, 0.0, {}

    votos: Dict[str, float] = {}
    for r in recuperados:
        votos[r.caso.diagnostico] = votos.get(r.caso.diagnostico, 0.0) + r.similaridade

    diagnostico_sugerido = max(votos, key=votos.get)
    confianca = votos[diagnostico_sugerido] / sum(votos.values())

    # tratamento herdado do caso mais similar que possui o diagnóstico vencedor
    candidatos = [r for r in recuperados if r.caso.diagnostico == diagnostico_sugerido]
    melhor = max(candidatos, key=lambda r: r.similaridade)
    tratamento_sugerido = melhor.caso.tratamento

    return diagnostico_sugerido, tratamento_sugerido, confianca, votos


def revise(diagnostico_sugerido: str, tratamento_sugerido: str,
           confirmado: bool, diagnostico_corrigido: Optional[str] = None,
           tratamento_corrigido: Optional[str] = None) -> Tuple[str, str]:
    """
    ETAPA 3 - REVISE
    Recebe a decisão humana (confirmação ou correção) sobre a sugestão e
    devolve o par (diagnóstico final, tratamento final) que será retido.
    """
    if confirmado:
        return diagnostico_sugerido, tratamento_sugerido
    diagnostico_final = diagnostico_corrigido or diagnostico_sugerido
    tratamento_final = tratamento_corrigido or tratamento_sugerido
    return diagnostico_final, tratamento_final


def retain(base: BaseDeCasos, consulta: Dict, diagnostico_final: str,
           tratamento_final: str, eficaz: bool = True) -> Caso:
    """
    ETAPA 4 - RETAIN
    Cria um novo caso a partir da consulta + solução validada/corrigida e o
    adiciona (persistindo) à base de casos, permitindo aprendizado contínuo.
    """
    novo_caso = Caso(
        id=f"R-{uuid.uuid4().hex[:8]}",
        sintomas=list(consulta.get("sintomas", [])),
        idade_faixa=consulta.get("idade_faixa", "adulto"),
        duracao_dias=consulta.get("duracao_dias", 0),
        diagnostico=diagnostico_final,
        tratamento=tratamento_final,
        eficaz=eficaz,
        origem="retido",
    )
    base.casos.append(novo_caso)
    base.salvar()
    return novo_caso


# --------------------------------------------------------------------------- #
# 6. FUNÇÃO DE CONVENIÊNCIA: executa o ciclo completo de forma não-interativa
#    (útil para testes automatizados e para o relatório técnico)
# --------------------------------------------------------------------------- #

def executar_ciclo_automatico(base: BaseDeCasos, consulta: Dict, top_k: int = 3,
                               aceitar_sugestao: bool = True,
                               diagnostico_corrigido: Optional[str] = None,
                               tratamento_corrigido: Optional[str] = None,
                               reter: bool = True) -> Dict:
    """Executa retrieve -> reuse -> revise -> retain sem interação via teclado."""
    recuperados = retrieve(base, consulta, top_k=top_k)
    diag_sug, trat_sug, confianca, votos = reuse(recuperados)
    diag_final, trat_final = revise(diag_sug, trat_sug, aceitar_sugestao,
                                     diagnostico_corrigido, tratamento_corrigido)
    novo_caso = None
    if reter:
        novo_caso = retain(base, consulta, diag_final, trat_final)

    return {
        "consulta": consulta,
        "recuperados": [(r.caso.id, r.caso.diagnostico, round(r.similaridade, 3)) for r in recuperados],
        "diagnostico_sugerido": diag_sug,
        "tratamento_sugerido": trat_sug,
        "confianca": round(confianca, 3),
        "votos": {k: round(v, 3) for k, v in votos.items()},
        "diagnostico_final": diag_final,
        "tratamento_final": trat_final,
        "novo_caso_id": novo_caso.id if novo_caso else None,
    }
