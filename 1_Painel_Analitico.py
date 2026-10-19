import json

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Painel Socioeconômico do Piauí",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Injeção de CSS Customizado (Design Profissional)
# -----------------------------
st.markdown("""
<style>
/* Estilização avançada para os cartões de métricas (Visão Geral) */
[data-testid="stMetric"] {
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 12px;
    padding: 20px;
    background-color: rgba(128, 128, 128, 0.03);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    border-color: rgba(0, 114, 178, 0.4);
}
[data-testid="stMetricLabel"] {
    font-weight: 600;
    font-size: 1.05rem;
    color: #555;
}

/* Ajuste no modo escuro para os cartões de métrica não ficarem muito claros */
@media (prefers-color-scheme: dark) {
    [data-testid="stMetricLabel"] {
        color: #ddd;
    }
}
</style>
""", unsafe_allow_html=True)

PALETA_ACESSIVEL = [
    "#0072B2", "#E69F00", "#009E73",
    "#CC79A7", "#56B4E9", "#D55E00"
]

INDICADORES = {
    "pib_per_capita": {
        "rotulo": "PIB per capita",
        "formato": "R$ {:,.2f}"
    },
    "pib_total": {
        "rotulo": "PIB total",
        "formato": "R$ {:,.0f}"
    },
    "populacao": {
        "rotulo": "População",
        "formato": "{:,.0f}"
    }
}

@st.cache_data
def carregar_dados():
    base = pd.read_parquet("data/processed/base_piaui.parquet")
    setores = pd.read_parquet("data/processed/setores_piaui.parquet")

    with open("data/geo/piaui_municipios.geojson", encoding="utf-8") as arquivo:
        geojson = json.load(arquivo)

    return base, setores, geojson

base, setores, geojson = carregar_dados()

st.title("📊 Painel Socioeconômico Municipal do Piauí")
st.caption(
    "Análise interativa dos 224 municípios piauienses. "
    "Fontes: IBGE/SIDRA — PIB Municipal (Tabela 5938) e "
    "População Residente Estimada (Tabela 6579)."
)
st.write("") 

# -----------------------------
# Filtros globais (Sidebar Profissionalizada)
# -----------------------------
st.sidebar.header("Filtros")

indicador = st.sidebar.selectbox(
    "Indicador do mapa e ranking",
    list(INDICADORES.keys()),
    format_func=lambda x: INDICADORES[x]["rotulo"]
)

faixa_selecionada = st.sidebar.selectbox(
    "Faixa de PIB per capita",
    [
        "Todas as faixas",
        "Menos de R$ 10.000",
        "Entre R$ 10.000 e R$ 15.000",
        "Entre R$ 15.000 e R$ 20.000",
        "Entre R$ 20.000 e R$ 30.000",
        "Acima de R$ 30.000"
    ]
)

# Lógica de filtragem categórica
if faixa_selecionada == "Menos de R$ 10.000":
    base_filtrada = base[base["pib_per_capita"] < 10000].copy()
elif faixa_selecionada == "Entre R$ 10.000 e R$ 15.000":
    base_filtrada = base[base["pib_per_capita"].between(10000, 14999.99)].copy()
elif faixa_selecionada == "Entre R$ 15.000 e R$ 20.000":
    base_filtrada = base[base["pib_per_capita"].between(15000, 19999.99)].copy()
elif faixa_selecionada == "Entre R$ 20.000 e R$ 30.000":
    base_filtrada = base[base["pib_per_capita"].between(20000, 29999.99)].copy()
elif faixa_selecionada == "Acima de R$ 30.000":
    base_filtrada = base[base["pib_per_capita"] >= 30000].copy()
else:
    base_filtrada = base.copy()

municipios_disponiveis = ["Todos os municípios"] + sorted(
    base_filtrada["municipio"].unique().tolist()
)

municipio_selecionado = st.sidebar.selectbox(
    "Município em destaque",
    municipios_disponiveis
)

# Verifica se a base filtrada ficou vazia para não quebrar o painel
if base_filtrada.empty:
    st.warning("Nenhum município encontrado nesta faixa de PIB per capita. Ajuste o filtro lateral.")
    st.stop()

# -----------------------------
# Indicadores gerais
# -----------------------------
st.subheader("Visão geral", divider="gray")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Municípios exibidos", len(base_filtrada))
col2.metric("População total", f"{base_filtrada['populacao'].sum():,.0f}".replace(",", "."))
col3.metric("PIB total", f"R$ {base_filtrada['pib_total'].sum() / 1e9:,.2f} bi".replace(",", "."))
col4.metric("PIB per capita médio", f"R$ {base_filtrada['pib_per_capita'].mean():,.0f}".replace(",", "."))

st.write("")
st.write("")

# -----------------------------
# Visão 1 — Mapa coroplético
# -----------------------------
with st.container(border=True):
    st.subheader("1. Visão geral espacial")
    
    fig_mapa = px.choropleth(
        base_filtrada,
        geojson=geojson,
        featureidkey="properties.cod_municipio",
        locations="cod_municipio",
        color=indicador,
        color_continuous_scale="Viridis",
        hover_name="municipio",
        hover_data={
            "cod_municipio": False,
            "populacao": ":,.0f",
            "pib_total": ":,.2f",
            "pib_per_capita": ":,.2f"
        },
        labels={
            "pib_per_capita": "PIB per capita (R$)",
            "pib_total": "PIB total (R$)",
            "populacao": "População"
        }
    )

    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(
        height=540,
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(title=INDICADORES[indicador]["rotulo"])
    )

    evento_mapa = st.plotly_chart(
        fig_mapa,
        use_container_width=True,
        on_select="rerun",
        selection_mode=["points"],
        key="mapa_piaui"
    )

# -----------------------------
# Lógica de Seleção Coordenada
# -----------------------------
codigos_selecionados = []

if evento_mapa and evento_mapa["selection"]["points"]:
    for ponto in evento_mapa["selection"]["points"]:
        codigo = ponto.get("location")
        if codigo:
            codigos_selecionados.append(str(codigo))

if municipio_selecionado != "Todos os municípios":
    codigo_lateral = base.loc[
        base["municipio"] == municipio_selecionado,
        "cod_municipio"
    ].iloc[0]
    codigos_selecionados = [str(codigo_lateral)]

if codigos_selecionados:
    contexto = base[base["cod_municipio"].isin(codigos_selecionados)].copy()
else:
    contexto = base_filtrada.copy()

# -----------------------------
# Visão 2 — Ranking municipal
# -----------------------------
with st.container(border=True):
    st.subheader("2. Ranking dos municípios")
    
    quantidade = st.slider(
        "Municípios exibidos no ranking",
        min_value=5, max_value=50, value=20
    )

    ranking = (
        base_filtrada
        .dropna(subset=[indicador])
        .nlargest(quantidade, indicador)
        .sort_values(indicador)
    )

    fig_ranking = px.bar(
        ranking,
        x=indicador,
        y="municipio",
        orientation="h",
        color=indicador,
        color_continuous_scale="Viridis",
        hover_data={
            "populacao": ":,.0f",
            "pib_total": ":,.2f",
            "pib_per_capita": ":,.2f",
            "municipio": False
        },
        labels={
            "pib_per_capita": "PIB per capita (R$)",
            "pib_total": "PIB total (R$)",
            "populacao": "População",
            "municipio": "Município"
        }
    )

    fig_ranking.update_layout(
        height=540,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )

    st.plotly_chart(fig_ranking, use_container_width=True, key="ranking_piaui")

# -----------------------------
# Visão 3 — Composição setorial
# -----------------------------
with st.container(border=True):
    st.subheader("3. Composição setorial do PIB")
    
    setores_contexto = setores[
        setores["cod_municipio"].isin(contexto["cod_municipio"])
    ].copy()

    if setores_contexto.empty:
        st.info("Selecione um município para exibir sua composição setorial.")
    elif setores_contexto["valor"].sum() <= 0:
        st.warning("Os dados setoriais deste município estão zerados ou preliminares na base do IBGE.")
    else:
        composicao = setores_contexto.groupby("setor", as_index=False)["valor"].sum()
        composicao = composicao[composicao["valor"] > 0]

        fig_setores = px.pie(
            composicao,
            names="setor",
            values="valor",
            hole=0.45,
            color_discrete_sequence=PALETA_ACESSIVEL
        )

        fig_setores.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:,.2f}<extra></extra>"
        )

        fig_setores.update_layout(
            height=440,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig_setores, use_container_width=True)

# -----------------------------
# Visão 4 — Detalhes sob demanda
# -----------------------------
with st.container(border=True):
    st.subheader("4. Detalhes sob demanda")
    
    if codigos_selecionados:
        st.success("Município(s) selecionado(s): " + ", ".join(contexto["municipio"].tolist()))
    else:
        st.info("Selecione um município no mapa ou na barra lateral para visualizar os detalhes.")

    setores_pivot = setores.pivot(
        index="cod_municipio", 
        columns="setor", 
        values="valor"
    ).reset_index()

    contexto_expandido = contexto.merge(setores_pivot, on="cod_municipio", how="left")

    setores_esperados = ["Agropecuária", "Indústria", "Serviços", "Administração Pública"]
    for col in setores_esperados:
        if col not in contexto_expandido.columns:
            contexto_expandido[col] = pd.NA

    tabela = contexto_expandido[[
        "municipio", "populacao", "pib_total", "pib_per_capita",
        "Agropecuária", "Indústria", "Serviços", "Administração Pública"
    ]].rename(columns={
        "municipio": "Município",
        "populacao": "População",
        "pib_total": "PIB total (R$)",
        "pib_per_capita": "PIB per capita (R$)",
        "Agropecuária": "Agropecuária (R$)",
        "Indústria": "Indústria (R$)",
        "Serviços": "Serviços (R$)",
        "Administração Pública": "Adm. Pública (R$)"
    })

    def formatar_inteiro_br(valor):
        if pd.isna(valor): return "-"
        return f"{valor:,.0f}".replace(",", ".")

    def formatar_moeda_br(valor):
        if pd.isna(valor): return "-"
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    colunas_numericas = [
        "População", "PIB total (R$)", "PIB per capita (R$)", 
        "Agropecuária (R$)", "Indústria (R$)", "Serviços (R$)", "Adm. Pública (R$)"
    ]

    tabela_estilizada = tabela.style.format({
        "População": formatar_inteiro_br,
        "PIB total (R$)": formatar_moeda_br,
        "PIB per capita (R$)": formatar_moeda_br,
        "Agropecuária (R$)": formatar_moeda_br,
        "Indústria (R$)": formatar_moeda_br,
        "Serviços (R$)": formatar_moeda_br,
        "Adm. Pública (R$)": formatar_moeda_br
    }).set_properties(
        subset=["Município"], **{"text-align": "left"}
    ).set_properties(
        subset=colunas_numericas, **{"text-align": "right"}
    ).set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#0072B2"),
                ("color", "white"),
                ("text-align", "center !important"),
                ("font-weight", "bold"),
                ("font-family", "sans-serif"),
                ("padding", "10px")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("padding", "8px"),
                ("border-bottom", "1px solid #ddd"),
                ("font-family", "sans-serif")
            ]
        }
    ]).hide(axis="index")

    html_tabela = tabela_estilizada.set_table_attributes(
        'style="width: 100%; border-collapse: collapse;"'
    ).to_html()

    st.markdown(html_tabela, unsafe_allow_html=True)
    st.write("")

    st.download_button(
        label="Baixar dados em CSV",
        data=contexto_expandido.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name="dados_filtrados_piaui.csv",
        mime="text/csv",
        type="primary"
    )

st.divider()
st.caption(
    "Desenvolvido com Streamlit e Plotly. "
    "Paleta e escala cromática selecionadas para melhor acessibilidade visual."
)