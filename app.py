import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


URL_VENDAS = (
    "https://raw.githubusercontent.com/alvarolucio2007/Engenharia-de-Software/"
    "refs/heads/main/4Periodo/CienciaDeDados/ACE/Receipt%20Transactions0.csv"
)
URL_SERVICOS = (
    "https://raw.githubusercontent.com/alvarolucio2007/Engenharia-de-Software/"
    "refs/heads/main/4Periodo/CienciaDeDados/ACE/Service%20Listing0.csv"
)

st.set_page_config(page_title="Análise de Vendas e Serviços", page_icon="📊", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data(show_spinner=False)
def carregar_url(url: str) -> pd.DataFrame:
    return pd.read_csv(url)


def carregar_upload(arquivo) -> pd.DataFrame:
    return pd.read_csv(arquivo)


def limpar_vendas(df: pd.DataFrame, normalizar_valores: bool) -> pd.DataFrame:
    resultado = df.drop_duplicates(keep="first").copy()
    if normalizar_valores and {"Description", "Amount"}.issubset(resultado.columns):
        descricao = resultado["Description"].astype("string").str.strip().str.lower()
        # `str` pode produzir valores ausentes do tipo pd.NA. Preencha a
        # máscara antes de convertê-la para NumPy para evitar truth-value errors.
        eh_miscellaneous = descricao.eq("miscellaneous").fillna(False).to_numpy(dtype=bool)
        valores = pd.to_numeric(resultado["Amount"], errors="coerce")
        resultado["Amount"] = np.where(eh_miscellaneous, valores, valores.abs())
    return resultado


def limpar_servicos(df: pd.DataFrame, remover_custo_zero: bool) -> pd.DataFrame:
    resultado = df.dropna().copy()
    if remover_custo_zero and "Cost" in resultado.columns:
        resultado = resultado[resultado["Cost"] != 0]
    return resultado


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def mostrar_resumo(df: pd.DataFrame, nome: str) -> None:
    c1, c2, c3 = st.columns(3)
    c1.metric("Registros", f"{len(df):,}".replace(",", "."))
    c2.metric("Colunas", len(df.columns))
    c3.metric("Células vazias", int(df.isna().sum().sum()))
    with st.expander(f"Inspeção da base de {nome.lower()}"):
        st.write("**Tipos de dados**")
        st.dataframe(df.dtypes.astype(str).rename("Tipo").to_frame(), use_container_width=True)
        st.write("**Valores ausentes por coluna**")
        st.dataframe(df.isna().sum().rename("Ausentes").to_frame(), use_container_width=True)
        st.write("**Duplicatas completas**", int(df.duplicated().sum()))
        st.dataframe(df.head(20), use_container_width=True)


def pagina_vendas(df_original: pd.DataFrame, normalizar: bool) -> None:
    df = limpar_vendas(df_original, normalizar)
    st.subheader("Vendas")
    mostrar_resumo(df, "vendas")

    if "Amount" in df.columns:
        valores = pd.to_numeric(df["Amount"], errors="coerce")
        a, b, c = st.columns(3)
        a.metric("Valor total", f"{valores.sum():,.2f}")
        b.metric("Valor médio", f"{valores.mean():,.2f}")
        c.metric("Valores negativos", int((valores < 0).sum()))

    if {"Staff", "Amount"}.issubset(df.columns):
        grafico = df.copy()
        grafico["Amount"] = pd.to_numeric(grafico["Amount"], errors="coerce")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=grafico, x="Staff", y="Amount", alpha=0.65, ax=ax)
        ax.set_title("Valor das transações por funcionário")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("O gráfico por funcionário requer as colunas `Staff` e `Amount`.")

    st.download_button(
        "Baixar vendas tratadas (CSV)", csv_bytes(df), "vendas_limpo.csv", "text/csv"
    )


def pagina_servicos(df_original: pd.DataFrame, remover_custo_zero: bool) -> None:
    df = limpar_servicos(df_original, remover_custo_zero)
    st.subheader("Catálogo de serviços")
    mostrar_resumo(df, "serviços")

    obrigatorias = {"Cost", "Price"}
    if not obrigatorias.issubset(df.columns):
        st.info("Os gráficos do catálogo requerem as colunas `Cost` e `Price`.")
    else:
        grafico = df.copy()
        grafico["Cost"] = pd.to_numeric(grafico["Cost"], errors="coerce")
        grafico["Price"] = pd.to_numeric(grafico["Price"], errors="coerce")
        hue = "Cate" if "Cate" in grafico.columns else None
        style = "IsActive" if "IsActive" in grafico.columns else None

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(
            data=grafico, x="Cost", y="Price", hue=hue, style=style,
            alpha=0.8, s=80, ax=ax,
        )
        ax.set_title("Relação entre custo e preço")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        if "Cate" in grafico.columns:
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.boxplot(data=grafico, x="Cate", y="Price", hue=style, ax=ax)
            ax.set_title("Distribuição de preços por categoria")
            ax.tick_params(axis="x", rotation=45)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.countplot(
                data=grafico, x="Cate", hue=style,
                order=grafico["Cate"].value_counts().index, ax=ax,
            )
            ax.set_title("Quantidade de itens por categoria")
            ax.tick_params(axis="x", rotation=45)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    st.download_button(
        "Baixar catálogo tratado (CSV)", csv_bytes(df), "servicos_limpos.csv", "text/csv"
    )


st.title("📊 Análise de Vendas e Serviços")
st.caption("Explore, limpe e baixe as bases usadas no notebook PIPELINE.ipynb.")

with st.sidebar:
    st.header("Dados de entrada")
    origem = st.radio("Origem dos CSVs", ["URLs do projeto", "Enviar meus arquivos"])
    arquivo_vendas = arquivo_servicos = None
    if origem == "Enviar meus arquivos":
        arquivo_vendas = st.file_uploader("CSV de vendas", type="csv", key="vendas")
        arquivo_servicos = st.file_uploader("CSV de serviços", type="csv", key="servicos")
    st.divider()
    normalizar_valores = st.checkbox(
        "Normalizar valores negativos das vendas", value=True,
        help="Aplica valor absoluto em Amount, preservando os registros miscellaneous.",
    )
    remover_custo_zero = st.checkbox("Remover serviços com custo zero", value=True)

try:
    if origem == "URLs do projeto":
        with st.spinner("Carregando os CSVs do GitHub..."):
            vendas = carregar_url(URL_VENDAS)
            servicos = carregar_url(URL_SERVICOS)
    else:
        if arquivo_vendas is None or arquivo_servicos is None:
            st.info("Envie os dois arquivos CSV na barra lateral para iniciar a análise.")
            st.stop()
        vendas = carregar_upload(arquivo_vendas)
        servicos = carregar_upload(arquivo_servicos)
except Exception as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.info("Verifique a conexão ou envie os CSVs manualmente pela barra lateral.")
    st.stop()

aba_vendas, aba_servicos = st.tabs(["Vendas", "Serviços"])
with aba_vendas:
    pagina_vendas(vendas, normalizar_valores)
with aba_servicos:
    pagina_servicos(servicos, remover_custo_zero)
