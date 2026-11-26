import numpy as np
import pandas as pd
import streamlit as st


URL_VENDAS = (
    "https://raw.githubusercontent.com/alvarolucio2007/Engenharia-de-Software/"
    "refs/heads/main/4Periodo/CienciaDeDados/ACE/Receipt%20Transactions0.csv"
)
URL_SERVICOS = (
    "https://raw.githubusercontent.com/alvarolucio2007/Engenharia-de-Software/"
    "refs/heads/main/4Periodo/CienciaDeDados/ACE/Service%20Listing0.csv"
)


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
