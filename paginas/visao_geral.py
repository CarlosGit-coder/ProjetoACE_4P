import streamlit as st

from componentes.ui import cabecalho_pagina, mostrar_resumo


def pagina_visao_geral(vendas, servicos) -> None:
    """Apresenta uma inspeção inicial das duas bases carregadas."""
    cabecalho_pagina(
        "Visão geral",
        "Confira a qualidade e o tamanho das bases antes de explorar os indicadores.",
    )
    esquerda, direita = st.columns(2)
    with esquerda:
        mostrar_resumo(vendas, "vendas")
    with direita:
        mostrar_resumo(servicos, "serviços")
