# Testes simples. Para rodar: python testes.py
from sistema_especialista import REGRAS, montar_fatos, inferir


def diagnosticar(respostas):
    fatos = montar_fatos(respostas)
    inferir(fatos)
    return fatos


def teste_tem_pelo_menos_20_regras():
    assert len(REGRAS) >= 20


def teste_tela_quebrada():
    assert "diag_tela" in diagnosticar({"tela_quebrada": "s"})


def teste_encadeamento_liquido():
    # liquido -> suspeita_oxidacao -> diag_liquido -> urgencia_alta
    fatos = diagnosticar({"liquido": "s", "liga": "n", "dados_importantes": "s"})
    assert "suspeita_oxidacao" in fatos
    assert "diag_liquido" in fatos
    assert "urgencia_alta" in fatos
    assert "recomenda_recuperar_dados" in fatos


def teste_bateria_inchada_e_critica():
    assert "urgencia_critica" in diagnosticar({"bateria_inchada": "s"})


def teste_garantia_perdida_por_queda():
    assert "fora_garantia" in diagnosticar({"garantia": "s", "queda": "s"})


def teste_nao_sei_nao_gera_conclusao():
    fatos = diagnosticar({"liga": "ns", "carrega": "ns"})
    assert not any(f.startswith("diag_") for f in fatos)


def teste_sem_conclusao():
    fatos = diagnosticar({"liga": "s", "imagem_tela": "s", "tela_quebrada": "n", "lento": "n"})
    assert not any(f.startswith("diag_") for f in fatos)


if __name__ == "__main__":
    testes = [f for nome, f in list(globals().items()) if nome.startswith("teste_")]
    for t in testes:
        t()
        print("OK ", t.__name__)
    print(f"\n{len(testes)} testes passaram.")



def teste_tela_quebrada_por_queda():
    assert "diag_tela_queda" in diagnosticar({"queda": "s", "tela_quebrada": "s"})
