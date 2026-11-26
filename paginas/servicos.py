import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from componentes.ui import cabecalho_pagina, csv_bytes, mostrar_resumo
from dados.loader import limpar_servicos


def pagina_servicos(df_original: pd.DataFrame, remover_custo_zero: bool) -> None:
    df = limpar_servicos(df_original, remover_custo_zero)
    cabecalho_pagina(
        "Catálogo de serviços",
        "Compare custo e preço e observe como os itens se distribuem por categoria.",
    )
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
        fig, ax = plt.subplots(figsize=(7, 3.8))
        sns.scatterplot(data=grafico, x="Cost", y="Price", hue=hue, style=style, alpha=0.8, s=70, ax=ax)
        ax.set_title("Relação entre custo e preço")
        fig.tight_layout()
        grafico_coluna, _ = st.columns([1, 1])
        with grafico_coluna:
            st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        if "Cate" in grafico.columns:
            coluna_box, coluna_contagem = st.columns(2)
            with coluna_box:
                fig, ax = plt.subplots(figsize=(6, 3.8))
                sns.boxplot(data=grafico, x="Cate", y="Price", hue=style, ax=ax)
                ax.set_title("Preços por categoria")
                ax.tick_params(axis="x", rotation=35)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            with coluna_contagem:
                fig, ax = plt.subplots(figsize=(6, 3.8))
                sns.countplot(data=grafico, x="Cate", hue=style, order=grafico["Cate"].value_counts().index, ax=ax)
                ax.set_title("Itens por categoria")
                ax.tick_params(axis="x", rotation=35)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

    st.download_button(
        "Baixar catálogo tratado (CSV)", csv_bytes(df), "servicos_limpos.csv", "text/csv"
    )
