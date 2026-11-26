import seaborn as sns
import streamlit as st

from dados.loader import (
    URL_SERVICOS,
    URL_VENDAS,
    carregar_upload,
    carregar_url,
)
from paginas.servicos import pagina_servicos
from paginas.vendas import pagina_vendas
from paginas.visao_geral import pagina_visao_geral


st.set_page_config(
    page_title="Análise de Vendas e Serviços",
    page_icon="📊",
    layout="wide",
)
sns.set_theme(
    style="darkgrid",
    palette="muted",
    rc={
        "figure.facecolor": "#1B252F",
        "axes.facecolor": "#1B252F",
        "axes.edgecolor": "#465460",
        "axes.labelcolor": "#D5DEE6",
        "text.color": "#E6EDF3",
        "xtick.color": "#C2CDD6",
        "ytick.color": "#C2CDD6",
        "grid.color": "#34414D",
    },
)


def obter_dados():
    """Exibe os controles de entrada e devolve as duas bases carregadas."""
    with st.sidebar:
        st.header("Dados de entrada")
        origem = st.radio("Origem dos CSVs", ["URLs do projeto", "Enviar meus arquivos"])
        arquivo_vendas = arquivo_servicos = None
        if origem == "Enviar meus arquivos":
            arquivo_vendas = st.file_uploader("CSV de vendas", type="csv", key="vendas")
            arquivo_servicos = st.file_uploader("CSV de serviços", type="csv", key="servicos")

        st.divider()
        normalizar_valores = st.checkbox(
            "Normalizar valores negativos das vendas",
            value=True,
            help="Aplica valor absoluto em Amount, preservando os registros miscellaneous.",
        )
        remover_custo_zero = st.checkbox("Remover serviços com custo zero", value=True)

    if origem == "Enviar meus arquivos":
        if arquivo_vendas is None or arquivo_servicos is None:
            st.info("Envie os dois arquivos CSV na barra lateral para iniciar a análise.")
            st.stop()
        return (
            carregar_upload(arquivo_vendas),
            carregar_upload(arquivo_servicos),
            normalizar_valores,
            remover_custo_zero,
        )

    with st.spinner("Carregando os CSVs do GitHub..."):
        return (
            carregar_url(URL_VENDAS),
            carregar_url(URL_SERVICOS),
            normalizar_valores,
            remover_custo_zero,
        )


st.title("📊 Análise de Vendas e Serviços")
st.caption("Uma leitura prática das transações e do catálogo de serviços.")

try:
    vendas, servicos, normalizar_valores, remover_custo_zero = obter_dados()
except Exception as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.info("Verifique a conexão ou envie os CSVs manualmente pela barra lateral.")
    st.stop()

aba_resumo, aba_vendas, aba_servicos = st.tabs(
    ["Visão geral", "Vendas", "Catálogo de serviços"]
)
with aba_resumo:
    pagina_visao_geral(vendas, servicos)
with aba_vendas:
    pagina_vendas(vendas, normalizar_valores)
with aba_servicos:
    pagina_servicos(servicos, remover_custo_zero)
