import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def csv_bytes(df: pd.DataFrame) -> bytes:
    """Converte uma tabela em bytes CSV para o botão de download."""
    return df.to_csv(index=False).encode("utf-8-sig")


def mostrar_resumo(df: pd.DataFrame, nome: str) -> None:
    """Mostra métricas rápidas e detalhes de qualidade de uma base."""
    c1, c2, c3 = st.columns(3)
    c1.metric("Linhas", f"{len(df):,}".replace(",", "."))
    c2.metric("Colunas", f"{len(df.columns):,}".replace(",", "."))
    c3.metric("Valores ausentes", f"{int(df.isna().sum().sum()):,}".replace(",", "."))
    with st.expander(f"Inspeção da base de {nome.lower()}"):
        st.write("**Tipos de dados**")
        st.dataframe(df.dtypes.astype(str).rename("Tipo").to_frame(), use_container_width=True)
        st.write("**Valores ausentes por coluna**")
        st.dataframe(df.isna().sum().rename("Ausentes").to_frame(), use_container_width=True)
        st.write("**Duplicatas completas**", int(df.duplicated().sum()))
        st.dataframe(df.head(20), use_container_width=True)


def cabecalho_pagina(titulo: str, descricao: str) -> None:
    """Padroniza o início das páginas de análise."""
    st.subheader(titulo)
    st.caption(descricao)
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def csv_bytes(df: pd.DataFrame) -> bytes:
    """Converte uma tabela em bytes CSV para o botão de download."""
    return df.to_csv(index=False).encode("utf-8-sig")


def mostrar_resumo(df: pd.DataFrame, nome: str) -> None:
    """Mostra métricas rápidas e detalhes de qualidade de uma base."""
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
