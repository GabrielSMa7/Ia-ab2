ATRIBUTOS = [
    (0, "É mamífero?"),
    (1, "Vive na água?"),
    (2, "Tem asas?"),
    (3, "É carnívoro?"),
    (4, "É herbívoro?"),
    (5, "Vive em ambientes urbanos?"),
    (6, "Tem pelos?"),
    (7, "Consegue voar?"),
    (8, "É ovíparo (põe ovos)?"),
    (9, "Vive em grupo?"),
    (10, "É maior que um humano adulto?"),
    (11, "É peçonhento ou venenoso?"),
    (12, "Tem hábitos noturnos?"),
    (13, "Vive em árvores?"),
    (14, "É réptil?"),
    (15, "Tem penas?"),
    (16, "É invertebrado?"),
    (17, "Possui 4 patas?"),
    (18, "É comum como animal de estimação?"),
    (19, "Vive em regiões frias ou gelo?"),
]

ID_PERGUNTA = {desc: id_ for id_, desc in ATRIBUTOS}

ANIMAIS = {
    "Cachorro": {
        "descricao": "Mamífero domesticado, conhecido como melhor amigo do homem.",
        "atributos": {
            0: True, 1: False, 2: False, 3: True, 4: False,
            5: True, 6: True, 7: False, 8: False, 9: True,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: True, 19: False,
        },
    },
    "Gato": {
        "descricao": "Felino domesticado, independente e muito popular como pet.",
        "atributos": {
            0: True, 1: False, 2: False, 3: True, 4: False,
            5: True, 6: True, 7: False, 8: False, 9: False,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: True, 19: False,
        },
    },
    "Leão": {
        "descricao": "Grande felino africano, conhecido como o rei da selva.",
        "atributos": {
            0: True, 1: False, 2: False, 3: True, 4: False,
            5: False, 6: True, 7: False, 8: False, 9: True,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: False, 19: False,
        },
    },
    "Elefante": {
        "descricao": "Maior mamífero terrestre, possui tromba e grandes orelhas.",
        "atributos": {
            0: True, 1: False, 2: False, 3: False, 4: True,
            5: False, 6: True, 7: False, 8: False, 9: True,
            10: True, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: False, 19: False,
        },
    },
    "Golfinho": {
        "descricao": "Mamífero marinho inteligente e conhecido por sua sociabilidade.",
        "atributos": {
            0: True, 1: True, 2: False, 3: True, 4: False,
            5: False, 6: False, 7: False, 8: False, 9: True,
            10: False, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: False, 17: False, 18: False, 19: False,
        },
    },
    "Águia": {
        "descricao": "Ave de rapina de grande porte, símbolo de força e visão aguçada.",
        "atributos": {
            0: False, 1: False, 2: True, 3: True, 4: False,
            5: False, 6: False, 7: True, 8: True, 9: False,
            10: False, 11: False, 12: False, 13: False, 14: False,
            15: True, 16: False, 17: False, 18: False, 19: False,
        },
    },
    "Cobra": {
        "descricao": "Réptil alongado sem patas, que pode ser venenoso ou não.",
        "atributos": {
            0: False, 1: False, 2: False, 3: True, 4: False,
            5: False, 6: False, 7: False, 8: True, 9: False,
            10: False, 11: True, 12: True, 13: False, 14: True,
            15: False, 16: False, 17: False, 18: False, 19: False,
        },
    },
    "Tubarão": {
        "descricao": "Peixe cartilaginoso predador dos oceanos, tem dentes afiados.",
        "atributos": {
            0: False, 1: True, 2: False, 3: True, 4: False,
            5: False, 6: False, 7: False, 8: False, 9: True,
            10: False, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: False, 17: False, 18: False, 19: False,
        },
    },
    "Cavalo": {
        "descricao": "Grande mamífero herbívoro usado para montaria e trabalho rural.",
        "atributos": {
            0: True, 1: False, 2: False, 3: False, 4: True,
            5: False, 6: True, 7: False, 8: False, 9: True,
            10: False, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: True, 19: False,
        },
    },
    "Macaco": {
        "descricao": "Primata ágil que vive em árvores, parente próximo dos humanos.",
        "atributos": {
            0: True, 1: False, 2: False, 3: False, 4: True,
            5: False, 6: True, 7: False, 8: False, 9: True,
            10: False, 11: False, 12: False, 13: True, 14: False,
            15: False, 16: False, 17: False, 18: False, 19: False,
        },
    },
    "Urso": {
        "descricao": "Grande mamífero onívoro encontrado em florestas e regiões frias.",
        "atributos": {
            0: True, 1: False, 2: False, 3: True, 4: False,
            5: False, 6: True, 7: False, 8: False, 9: False,
            10: True, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: False, 19: True,
        },
    },
    "Lobo": {
        "descricao": "Canídeo selvagem que vive em alcateias e é ancestral do cão.",
        "atributos": {
            0: True, 1: False, 2: False, 3: True, 4: False,
            5: False, 6: True, 7: False, 8: False, 9: True,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: False, 19: True,
        },
    },
    "Borboleta": {
        "descricao": "Inseto voador de asas coloridas que passa por metamorfose.",
        "atributos": {
            0: False, 1: False, 2: True, 3: False, 4: True,
            5: True, 6: False, 7: True, 8: True, 9: False,
            10: False, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: True, 17: False, 18: False, 19: False,
        },
    },
    "Sapo": {
        "descricao": "Anfíbio de pele úmida que vive próximo à água e tem canto característico.",
        "atributos": {
            0: False, 1: True, 2: False, 3: True, 4: False,
            5: True, 6: False, 7: False, 8: True, 9: False,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: False, 19: False,
        },
    },
    "Aranha": {
        "descricao": "Aracnídeo de oito patas que tece teias para capturar presas.",
        "atributos": {
            0: False, 1: False, 2: False, 3: True, 4: False,
            5: True, 6: False, 7: False, 8: True, 9: False,
            10: False, 11: True, 12: True, 13: False, 14: False,
            15: False, 16: True, 17: False, 18: False, 19: False,
        },
    },
    "Polvo": {
        "descricao": "Molusco marinho inteligente com oito tentáculos e grande capacidade de camuflagem.",
        "atributos": {
            0: False, 1: True, 2: False, 3: True, 4: False,
            5: False, 6: False, 7: False, 8: True, 9: False,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: True, 17: False, 18: False, 19: True,
        },
    },
    "Pinguim": {
        "descricao": "Ave marinha que não voa, adaptada ao frio extremo da Antártida.",
        "atributos": {
            0: False, 1: True, 2: True, 3: True, 4: False,
            5: False, 6: False, 7: False, 8: True, 9: True,
            10: False, 11: False, 12: False, 13: False, 14: False,
            15: True, 16: False, 17: False, 18: False, 19: True,
        },
    },
    "Girafa": {
        "descricao": "Mamífero africano de pescoço longo, o animal mais alto do mundo.",
        "atributos": {
            0: True, 1: False, 2: False, 3: False, 4: True,
            5: False, 6: True, 7: False, 8: False, 9: True,
            10: True, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: False, 19: False,
        },
    },
    "Baleia": {
        "descricao": "Maior animal do planeta, mamífero marinho que pode atingir enormes dimensões.",
        "atributos": {
            0: True, 1: True, 2: False, 3: True, 4: False,
            5: False, 6: False, 7: False, 8: False, 9: True,
            10: True, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: False, 17: False, 18: False, 19: True,
        },
    },
    "Tatu": {
        "descricao": "Mamífero com carapaça dura, encontrado nas Américas, cava tocas.",
        "atributos": {
            0: True, 1: False, 2: False, 3: True, 4: False,
            5: True, 6: True, 7: False, 8: False, 9: False,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: False, 16: False, 17: True, 18: False, 19: False,
        },
    },
    "Coruja": {
        "descricao": "Ave de rapina noturna conhecida por sua capacidade de girar a cabeça.",
        "atributos": {
            0: False, 1: False, 2: True, 3: True, 4: False,
            5: True, 6: False, 7: True, 8: True, 9: False,
            10: False, 11: False, 12: True, 13: False, 14: False,
            15: True, 16: False, 17: False, 18: False, 19: False,
        },
    },
    "Jacaré": {
        "descricao": "Grande réptil aquático de mandíbula poderosa, vive em rios e pântanos.",
        "atributos": {
            0: False, 1: True, 2: False, 3: True, 4: False,
            5: False, 6: False, 7: False, 8: True, 9: True,
            10: False, 11: False, 12: True, 13: False, 14: True,
            15: False, 16: False, 17: True, 18: False, 19: False,
        },
    },
    "Formiga": {
        "descricao": "Inseto social que vive em colônias organizadas e carrega alimentos.",
        "atributos": {
            0: False, 1: False, 2: False, 3: False, 4: True,
            5: True, 6: False, 7: False, 8: True, 9: True,
            10: False, 11: False, 12: False, 13: False, 14: False,
            15: False, 16: True, 17: False, 18: False, 19: False,
        },
    },
}
