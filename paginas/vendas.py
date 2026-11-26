import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from componentes.ui import cabecalho_pagina, csv_bytes, mostrar_resumo
from dados.loader import limpar_vendas


def pagina_vendas(df_original: pd.DataFrame, normalizar: bool) -> None:
    df = limpar_vendas(df_original, normalizar)
    cabecalho_pagina(
        "Vendas",
        "Valores e distribuição das transações após aplicar as opções de tratamento.",
    )
    mostrar_resumo(df, "vendas")

    if "Amount" in df.columns:
        valores = pd.to_numeric(df["Amount"], errors="coerce")
        a, b, c = st.columns(3)
        a.metric("Valor total", f"{valores.sum():,.2f}", help="Soma dos valores numéricos de Amount.")
        b.metric("Valor médio", f"{valores.mean():,.2f}", help="Média dos valores numéricos de Amount.")
        c.metric("Valores negativos", f"{int((valores < 0).sum()):,}")

    if {"Staff", "Amount"}.issubset(df.columns):
        grafico = df.copy()
        grafico["Amount"] = pd.to_numeric(grafico["Amount"], errors="coerce")
        fig, ax = plt.subplots(figsize=(7, 3.8))
        sns.scatterplot(data=grafico, x="Staff", y="Amount", alpha=0.65, color="#70C1B3", ax=ax)
        ax.set_title("Valor das transações por funcionário")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        grafico_coluna, _ = st.columns([1, 1])
        with grafico_coluna:
            st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("O gráfico por funcionário requer as colunas `Staff` e `Amount`.")

    st.download_button(
        "Baixar vendas tratadas (CSV)", csv_bytes(df), "vendas_limpo.csv", "text/csv"
    )
