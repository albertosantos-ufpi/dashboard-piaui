import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Arquitetura do Painel",
    page_icon="🏗️",
    layout="wide"
)

# Estilização CSS adicional para os painéis de texto
st.markdown("""
<style>
    .info-box {
        background-color: rgba(128, 128, 128, 0.05);
        border-left: 4px solid #0072B2;
        padding: 15px 20px;
        margin-top: 15px;
        margin-bottom: 10px;
        border-radius: 0 8px 8px 0;
        font-size: 0.95rem;
    }
    .highlight {
        font-weight: 600;
        color: #0072B2;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Arquitetura e Estratégia Visual")
st.caption(
    "Detalhamento técnico, princípios de design e tecnologias adotadas no desenvolvimento "
    "do Painel Socioeconômico do Piauí."
)

st.write("") # Espaçamento inicial

# -----------------------------
# SEÇÃO 1: ARQUITETURA DE INTERAÇÃO
# -----------------------------
with st.container(border=True):
    st.subheader("1. Arquitetura de Interação")
    
    st.markdown("""
    A interface foi projetada sob o rigor do **Mantra de Busca Visual de Ben Shneiderman** 
    (*"Overview first, zoom and filter, then details-on-demand"*), garantindo um fluxo cognitivo lógico 
    para a exploração dos dados socioeconômicos dos 224 municípios piauienses.
    
    *   **Overview First (Visão Geral):** O mapa coroplético atua como o ponto de partida, oferecendo uma leitura macro da distribuição de riqueza e população no estado. Os cartões superiores resumem as grandezas consolidadas.
    *   **Zoom and Filter (Filtros e Foco):** A barra lateral permite fatiar os dados por faixas de PIB e selecionar indicadores.
    *   **Details-on-Demand (Detalhes sob Demanda):** A tabela estilizada e os *tooltips* (caixas flutuantes ao passar o mouse) revelam os números exatos e a composição setorial apenas quando o usuário requisita.
    """)

    st.markdown("""
    <div class="info-box">
        <span class="highlight">Coordenação de Múltiplas Visões (Brushing & Linking):</span> 
        O painel implementa interatividade bidirecional nativa. A seleção espacial (clicar em um município no mapa) 
        ou categórica (usar o seletor lateral) propaga-se instantaneamente, re-renderizando a composição setorial 
        (gráfico de pizza) e filtrando a matriz de detalhes (tabela).
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -----------------------------
# SEÇÃO 2: DESIGN E ACESSIBILIDADE VISUAL
# -----------------------------
with st.container(border=True):
    st.subheader("2. Design e Acessibilidade Visual")
    st.write("") # Espaçamento para as colunas respirarem
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👁️ Colorblind-Safe")
        st.markdown("""
        A escolha cromática do projeto prioriza a acessibilidade visual para usuários com deficiências na percepção de cores (daltonismo):
        
        *   **Escala Sequencial (Viridis):** Utilizada no mapa e no ranking. A paleta *Viridis* é perceptualmente uniforme (mudanças nos dados são percebidas visualmente de forma proporcional). Ela evolui do escuro ao claro, garantindo distinção por luminosidade para pessoas com deuteranopia, protanopia ou visão monocromática.
        *   **Cores Categóricas:** O gráfico de composição setorial utiliza tons inspirados na paleta de Okabe e Ito (Azul, Laranja, Verde-azulado, Vermelho-alaranjado), maximizando o contraste seguro.
        """)

    with col2:
        st.markdown("#### 📉 Proporção Tinta-Dado (Data-Ink Ratio)")
        st.markdown("""
        O painel busca a conformidade com o princípio documentado por **Edward Tufte**, que defende a maximização da tinta usada para exibir dados, eliminando elementos não-informativos:
        
        *   **Remoção de "Chartjunk":** Gráficos sem bordas espessas internas, sem grades de fundo desnecessárias e sem sombras 3D que distorcem as proporções.
        *   **Legendas Integradas:** Uso de *tooltips* interativos e rótulos diretos nas fatias, eliminando a necessidade de legendas laterais redundantes.
        *   **Containers Discretos:** Delimitação de seções com bordas extremamente finas e fundos neutros, permitindo que a cor destaque apenas os dados.
        """)

st.write("")

# -----------------------------
# SEÇÃO 3: STACK TECNOLÓGICO
# -----------------------------
with st.container(border=True):
    st.subheader("3. Stack Tecnológico e Engenharia de Dados")
    
    st.markdown("""
    O projeto foi construído utilizando uma arquitetura modularizada em Python, 
    separando a lógica de extração (ETL) da camada de visualização em tempo real.
    """)
    st.write("") # Espaçamento
    
    col_tech1, col_tech2, col_tech3 = st.columns(3)

    with col_tech1:
        st.markdown("##### 🏛️ Dados Oficiais (APIs)")
        st.markdown("""
        *   **IBGE / SIDRA:** Consumo automatizado da API Restful oficial.
        *   **Tabela 5938:** PIB a preços correntes e valor adicionado por setor econômico.
        *   **Tabela 6579:** Estimativas da população residente.
        *   **Malha Municipal:** Arquivos geográficos oficiais GeoJSON (2022).
        """)

    with col_tech2:
        st.markdown("##### ⚙️ Engenharia e ETL")
        st.markdown("""
        *   **Pandas:** Motor principal para limpeza, agregações setoriais (*groupby*) e enriquecimento da base geométrica.
        *   **Apache Parquet:** Formato de armazenamento colunar ultra-eficiente. Permite que o dashboard seja carregado na memória em milissegundos.
        *   **Rotinas de Tratamento:** Scripts que removem anomalias textuais e contornam lacunas nas divulgações preliminares do IBGE.
        """)

    with col_tech3:
        st.markdown("##### 📊 Front-end e InfoVis")
        st.markdown("""
        *   **Streamlit:** *Framework* responsável pelo roteamento web, gestão de estado dos filtros e layout de componentes.
        *   **Plotly Express:** Biblioteca declarativa (baseada em D3.js) que viabiliza a interatividade nativa e renderização geográfica (`px.choropleth`).
        *   **Pandas Styler:** Injeção de regras CSS sob medida para o alinhamento de precisão (casas decimais) nas matrizes contábeis.
        """)

st.write("")

# -----------------------------
# RODAPÉ
# -----------------------------
st.success(
    "**Conclusão:** O painel se estabelece não apenas como um visualizador de dados, mas como um "
    "**produto de dados analítico robusto**, que une as melhores práticas de engenharia de software "
    "com os mais altos padrões acadêmicos e profissionais de design da informação."
)