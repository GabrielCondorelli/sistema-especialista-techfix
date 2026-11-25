# Interface web do sistema especialista (usa o Streamlit)
# Para rodar: streamlit run app_web.py
import io
from contextlib import redirect_stdout

import streamlit as st

from sistema_especialista import PERGUNTAS, TEXTOS, montar_fatos, inferir, por_que, como


def capturar(funcao, *args):
    """As funções por_que e como usam print(). Aqui pegamos o texto em vez de imprimir."""
    saida = io.StringIO()
    with redirect_stdout(saida):
        funcao(*args)
    return saida.getvalue()


st.set_page_config(page_title="TechFix", page_icon="🔧")
st.title("🔧 TechFix Assistência Técnica")
st.write("Triagem inteligente: responda as perguntas e clique em **Diagnosticar**.")

# ---------- 1) Perguntas ----------
OPCOES = {"não sei": "ns", "sim": "s", "não": "n"}
respostas = {}
for fato, texto, so_se in PERGUNTAS:
    if so_se is not None and so_se not in montar_fatos(respostas):
        continue  # pergunta não se aplica (ex.: ventoinha em celular)
    # o "?" ao lado da pergunta mostra POR QUE ela é feita
    escolha = st.selectbox(texto, list(OPCOES), key=fato, help=capturar(por_que, fato))
    respostas[fato] = OPCOES[escolha]

# ---------- 2) Inferência e resultado ----------
if st.button("Diagnosticar", type="primary"):
    fatos = montar_fatos(respostas)
    explicacao = inferir(fatos)
    diagnosticos = sorted(f for f in fatos if f.startswith("diag_"))

    st.subheader("Resultado da triagem")
    if not diagnosticos:
        st.warning("Não foi possível concluir com as informações fornecidas. "
                   "Encaminhe o aparelho para avaliação presencial.")
    for d in diagnosticos:
        st.success(TEXTOS[d])
        with st.expander("Como cheguei nessa conclusão?"):
            st.code(capturar(como, d, explicacao), language=None)

    if diagnosticos:
        for fato in sorted(fatos):
            if fato == "urgencia_critica":
                st.error(TEXTOS[fato])
            elif fato == "urgencia_alta":
                st.warning(TEXTOS[fato])
            elif fato.startswith("recomenda_") or fato in ("fora_garantia", "possivel_garantia"):
                st.info(TEXTOS[fato])
