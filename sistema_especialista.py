# Sistema Especialista - Triagem de Assistência Técnica
# Empresa simulada: TechFix Assistência Técnica (celulares e notebooks)
#
# Problema de negócio: os atendentes fazem a triagem de forma diferente uns dos
# outros. O sistema padroniza: pergunta os sintomas, aplica regras, diz o
# diagnóstico provável, a urgência e explica como chegou nessa conclusão.


# 1) BASE DE CONHECIMENTO


# 
# 
PERGUNTAS = [
    ("notebook", "O aparelho é um notebook? (n = é celular)", None),
    ("garantia", "O aparelho está na garantia?", None),
    ("liga", "O aparelho liga?", None),
    ("carrega", "Ele reconhece o carregador / carrega a bateria?", None),
    ("imagem_tela", "Aparece imagem na tela?", "liga"),
    ("tela_quebrada", "A tela está trincada ou quebrada?", None),
    ("queda", "O aparelho sofreu queda ou pancada?", None),
    ("liquido", "O aparelho teve contato com líquido?", None),
    ("bateria_inchada", "A bateria está inchada (aparelho estufado)?", None),
    ("bateria_fraca", "A bateria está durando muito pouco?", None),
    ("esquenta", "O aparelho esquenta demais?", None),
    ("ventoinha_barulho", "A ventoinha faz barulho alto? (só notebook)", "notebook"),
    ("reinicia", "O aparelho reinicia sozinho?", "liga"),
    ("lento", "O aparelho está muito lento ou travando?", "liga"),
    ("espaco_cheio", "Aparece aviso de armazenamento cheio?", "liga"),
    ("anuncios", "Aparecem anúncios ou programas que você não instalou?", "liga"),
    ("erro_sistema", "Aparece tela azul ou erro de sistema?", "liga"),
    ("sem_wifi", "O aparelho não conecta ao Wi-Fi?", "liga"),
    ("dados_importantes", "Há dados importantes sem backup no aparelho?", None),
]

# Regras: SE todas as condições ("se") forem verdadeiras ENTÃO ("entao") é verdadeiro.
# Fatos que começam com "diag_" são diagnósticos.
REGRAS = [
    # --- suspeitas (conclusões intermediárias) ---
    {"id": "R01", "se": ["liquido"], "entao": "suspeita_oxidacao"},
    {"id": "R02", "se": ["nao_liga", "nao_carrega"], "entao": "suspeita_alimentacao"},
    # --- diagnósticos ---
    {"id": "R03", "se": ["tela_quebrada"], "entao": "diag_tela"},
    {"id": "R04", "se": ["suspeita_oxidacao", "nao_liga"], "entao": "diag_liquido"},
    {"id": "R05", "se": ["suspeita_alimentacao", "nao_liquido"], "entao": "diag_carregador"},
    {"id": "R06", "se": ["nao_liga", "carrega", "queda"], "entao": "diag_placa"},
    {"id": "R07", "se": ["nao_liga", "carrega", "nao_queda", "nao_liquido"], "entao": "diag_placa_ou_bateria"},
    {"id": "R08", "se": ["bateria_inchada"], "entao": "diag_bateria_inchada"},
    {"id": "R09", "se": ["bateria_fraca"], "entao": "diag_desgaste_bateria"},
    {"id": "R10", "se": ["lento", "espaco_cheio"], "entao": "diag_espaco_cheio"},
    {"id": "R11", "se": ["lento", "anuncios"], "entao": "diag_virus"},
    {"id": "R12", "se": ["lento", "nao_espaco_cheio", "nao_anuncios"], "entao": "diag_upgrade_ou_formatacao"},
    {"id": "R13", "se": ["esquenta", "ventoinha_barulho"], "entao": "diag_limpeza_cooler"},
    {"id": "R14", "se": ["reinicia", "esquenta"], "entao": "diag_superaquecimento"},
    {"id": "R15", "se": ["reinicia", "nao_esquenta"], "entao": "diag_software_ou_memoria"},
    {"id": "R16", "se": ["erro_sistema"], "entao": "diag_so_corrompido"},
    {"id": "R17", "se": ["sem_wifi", "nao_erro_sistema"], "entao": "diag_rede"},
    {"id": "R18", "se": ["liga", "nao_imagem_tela"], "entao": "diag_display"},
    # --- urgência (usam diagnósticos como condição: encadeamento) ---
    {"id": "R19", "se": ["diag_liquido"], "entao": "urgencia_alta"},
    {"id": "R20", "se": ["diag_bateria_inchada"], "entao": "urgencia_critica"},
    {"id": "R21", "se": ["diag_superaquecimento"], "entao": "urgencia_alta"},
    # --- recomendações ---
    {"id": "R22", "se": ["diag_liquido", "dados_importantes"], "entao": "recomenda_recuperar_dados"},
    {"id": "R23", "se": ["diag_so_corrompido", "dados_importantes"], "entao": "recomenda_backup"},
    {"id": "R24", "se": ["diag_virus", "dados_importantes"], "entao": "recomenda_backup"},
    # --- garantia ---
    {"id": "R25", "se": ["garantia", "queda"], "entao": "fora_garantia"},
    {"id": "R26", "se": ["garantia", "liquido"], "entao": "fora_garantia"},
    {"id": "R27", "se": ["garantia", "nao_queda", "nao_liquido"], "entao": "possivel_garantia"},
    {"id": "R28", "se": ["queda", "tela_quebrada"], "entao": "diag_tela_queda"},
]


# Textos mostrados ao cliente 
TEXTOS = {
    "diag_tela": "Tela danificada: troca de display (2 dias, R$ 250 a R$ 900)",
    "diag_liquido": "Dano por líquido: limpeza e reparo de placa (5 dias, R$ 150 a R$ 800)",
    "diag_carregador": "Conector de carga ou carregador defeituoso (2 dias, R$ 80 a R$ 350)",
    "diag_placa": "Placa-mãe danificada: reparo de placa (7 dias, R$ 300 a R$ 1500)",
    "diag_placa_ou_bateria": "Falha de placa ou bateria: testes de bancada (3 dias, R$ 150 a R$ 600)",
    "diag_bateria_inchada": "Bateria inchada: troca imediata (1 dia, R$ 120 a R$ 450)",
    "diag_desgaste_bateria": "Desgaste da bateria: troca de bateria (1 dia, R$ 100 a R$ 400)",
    "diag_espaco_cheio": "Armazenamento cheio: backup e limpeza (1 dia, até R$ 80)",
    "diag_virus": "Vírus ou adware: remoção e reinstalação segura (1 dia, R$ 60 a R$ 150)",
    "diag_upgrade_ou_formatacao": "Sistema degradado: formatação ou upgrade de SSD/RAM (1 dia, R$ 60 a R$ 600)",
    "diag_limpeza_cooler": "Cooler sujo: limpeza e troca de pasta térmica (2 dias, R$ 100 a R$ 250)",
    "diag_superaquecimento": "Superaquecimento com reinício: teste térmico (3 dias, R$ 150 a R$ 700)",
    "diag_software_ou_memoria": "Falha de software ou memória: testes e reinstalação (2 dias, R$ 80 a R$ 400)",
    "diag_so_corrompido": "Sistema operacional corrompido: formatação (1 dia, R$ 60 a R$ 150)",
    "diag_rede": "Problema de rede: configuração ou troca do módulo Wi-Fi (1 dia, até R$ 200)",
    "diag_display": "Display ou cabo flat com defeito (3 dias, R$ 150 a R$ 600)",
    "urgencia_alta": "URGÊNCIA ALTA: atender em até 24 horas",
    "urgencia_critica": "URGÊNCIA CRÍTICA: risco de incêndio, pare de usar o aparelho",
    "recomenda_recuperar_dados": "Recomendação: desligue o aparelho e priorize a recuperação de dados",
    "recomenda_backup": "Recomendação: faça backup dos dados antes de formatar",
    "fora_garantia": "Garantia: provável mau uso, serviço fora da garantia",
    "possivel_garantia": "Garantia: possível cobertura, encaminhar ao fabricante",
    "diag_tela_queda": "Tela quebrada por queda: troca de display e verificação da placa (3 dias, R$ 300 a R$ 1000)",
}


# 
# 2) MOTOR DE INFERÊNCIA 
#

def montar_fatos(respostas):
    """Transforma as respostas {fato: 's' ou 'n' ou 'ns'} em um conjunto de fatos."""
    fatos = set()
    for fato, resp in respostas.items():
        if resp == "s":
            fatos.add(fato)
        elif resp == "n":
            fatos.add("nao_" + fato)
        
    return fatos


def inferir(fatos):
    """Aplica as regras repetidamente até não surgir nenhum fato novo.

    Devolve um dicionário {fato novo: regra que o criou}, usado na explicação.
    """
    explicacao = {}
    surgiu_fato_novo = True
    while surgiu_fato_novo:
        surgiu_fato_novo = False
        for regra in REGRAS:
            ja_tem = regra["entao"] in fatos
            condicoes_ok = all(c in fatos for c in regra["se"])
            if condicoes_ok and not ja_tem:
                fatos.add(regra["entao"])
                explicacao[regra["entao"]] = regra
                surgiu_fato_novo = True
    return explicacao



# 3) EXPLICAÇÃO (por que / como)


def por_que(fato):
    """POR QUE a pergunta é feita: mostra as regras que usam aquele fato."""
    usadas = [r for r in REGRAS if fato in r["se"] or "nao_" + fato in r["se"]]
    if not usadas:
        print("Essa informação não é usada diretamente por nenhuma regra.")
        return
    print("Pergunto isso porque a resposta é usada nas regras:")
    for r in usadas:
        print(f"  {r['id']}: SE {' E '.join(r['se'])} ENTÃO {r['entao']}")


def como(fato, explicacao, nivel=0):
    """COMO o sistema concluiu um fato: mostra a regra e as condições, recursivamente."""
    recuo = "    " * nivel
    if fato not in explicacao:
        print(f"{recuo}- {fato}: informado pelo usuário")
        return
    regra = explicacao[fato]
    print(f"{recuo}- {fato}: concluído pela regra {regra['id']} "
          f"(SE {' E '.join(regra['se'])})")
    for condicao in regra["se"]:
        como(condicao, explicacao, nivel + 1)



# 4) INTERFACE DE CONSOLE


def perguntar(fato, texto):
    """Repete a pergunta até receber uma resposta válida (tratamento de entrada inválida)."""
    sinonimos = {"sim": "s", "nao": "n", "não": "n"}
    while True:
        resp = input(f"\n{texto}\n  (s = sim, n = não, ns = não sei, pq = por quê): ").strip().lower()
        resp = sinonimos.get(resp, resp)
        if resp in ("s", "n", "ns"):
            return resp
        if resp == "pq":
            por_que(fato)
        elif resp == "sair":
            raise SystemExit("Atendimento encerrado.")
        else:
            print("Entrada inválida. Digite s, n, ns ou pq.")


def coletar_respostas():
    respostas = {}
    fatos = set()
    for fato, texto, so_se in PERGUNTAS:
        if so_se is not None and so_se not in fatos:
            continue 
        resp = perguntar(fato, texto)
        respostas[fato] = resp
        fatos = montar_fatos(respostas)
    return respostas


def mostrar_resultado(fatos, explicacao):
    print("\n" + "=" * 60)
    print("RESULTADO DA TRIAGEM")
    print("=" * 60)
    diagnosticos = sorted(f for f in fatos if f.startswith("diag_"))
    if not diagnosticos:
        # tratamento de exceção: nenhuma regra levou a um diagnóstico
        print("Não foi possível concluir com as informações fornecidas.")
        print("Sugestão: encaminhar o aparelho para avaliação presencial.")
        return diagnosticos
    for numero, d in enumerate(diagnosticos, 1):
        print(f"{numero}) {TEXTOS[d]}")
    for fato in sorted(fatos):
        if fato.startswith(("urgencia_", "recomenda_")) or fato in ("fora_garantia", "possivel_garantia"):
            print(TEXTOS[fato])
    return diagnosticos


def main():
    print("=" * 60)
    print("TECHFIX ASSISTÊNCIA TÉCNICA - TRIAGEM INTELIGENTE")
    print("=" * 60)
    print("Digite 'pq' em uma pergunta para ver por que ela é feita.")
    respostas = coletar_respostas()
    fatos = montar_fatos(respostas)
    explicacao = inferir(fatos)
    diagnosticos = mostrar_resultado(fatos, explicacao)
    while diagnosticos:
        op = input("\nDigite o nº do diagnóstico para ver COMO cheguei nele (ENTER sai): ").strip()
        if op == "":
            break
        if op.isdigit() and 1 <= int(op) <= len(diagnosticos):
            como(diagnosticos[int(op) - 1], explicacao)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nAtendimento encerrado.")
