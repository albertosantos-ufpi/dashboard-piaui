import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Informações Acadêmicas",
    page_icon="🎓",
    layout="wide"
)

# Estilização CSS para o cabeçalho institucional
st.markdown("""
<style>
    .inst-header {
        text-align: center;
        font-weight: 800;
        color: #0072B2;
        margin-bottom: 5px;
        font-size: 1.8rem;
    }
    .inst-sub {
        text-align: center;
        font-size: 1.1rem;
        color: #555;
        font-weight: 500;
        margin-bottom: 25px;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='inst-header'>UNIVERSIDADE FEDERAL DO PIAUÍ — UFPI</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='inst-sub'>CENTRO DE EDUCAÇÃO ABERTA E A DISTÂNCIA — CEAD<br>CURSO TECNÓLOGO EM GESTÃO DE DADOS</div>", 
    unsafe_allow_html=True
)

st.divider()

col1, col2 = st.columns([1, 2.2], gap="large")

with col1:
    with st.container(border=True):
        st.subheader("📌 Identificação")
        st.write("")
        st.markdown("""
        **Disciplina:**  
        Introdução à Visualização da Informação (InfoVis)
        
        **Módulo/Semestre:**  
        2026.2
        
        **Professor:**  
        Prof. MSc. Wesley Geraldo de Oliveira da Nóbrega
        
        **Aluno:**  
        Alberto Andrade dos Santos
        
        **Matrícula:**  
        20259051703
        """)
        
    with st.container(border=True):
        st.subheader("🌐 Acesso Online")
        st.write("Ambiente de produção hospedado no **Streamlit Community Cloud**.")
        st.write("")
        
        st.markdown("**Link oficial:**")
        # Exibe a URL de forma explícita com botão de copiar embutido
        st.code("https://dashboard-piaui.streamlit.app/", language="text")
        
        # Mantém o botão de acesso rápido com destaque
        st.link_button(
            "🚀 Acessar Painel Publicado", 
            "https://dashboard-piaui.streamlit.app/", 
            type="primary", 
            use_container_width=True
        )

with col2:
    with st.container(border=True):
        st.subheader("💡 Sobre o Projeto")
        st.write("")
        st.markdown("""
        O presente painel analítico foi desenvolvido como instrumento prático de avaliação técnica para a disciplina de **Introdução à Visualização da Informação (InfoVis)**. O projeto materializa a aplicação de bibliotecas Python de alto desempenho na construção de interfaces gerenciais interativas e na manipulação de microdados oficiais.
        
        Dentre os recursos implementados, destacam-se:
        
        * **Engenharia e Persistência de Dados (ETL):** Uso intensivo da biblioteca `Pandas` para extração (via API Restful do IBGE), limpeza, tratamento de nulidades e formatação de indicadores econômicos. A base consolidada é persistida localmente no formato colunar de alta compactação **Apache Parquet**, garantindo tempo de resposta instantâneo na renderização web.
        * **Visualização Espacial:** O geoprocessamento é conduzido pela união dos dados tabulares com malhas geográficas oficiais do IBGE em formato **GeoJSON**, renderizadas por meio da biblioteca `Plotly Express` (geração de mapas coropléticos responsivos).
        * **Coordenação Dinâmica (Brushing & Linking):** O sistema implementa uma arquitetura avançada de estado global utilizando os gatilhos nativos de recarregamento do `Streamlit` (`on_select`). Qualquer ação isolada — seja a seleção espacial direta nos polígonos do mapa ou o filtro categórico no painel de controle — atua como cruzamento primário, propagando e atualizando simultaneamente todos os demais cartões de métricas, gráficos setoriais e detalhamentos tabulares sob demanda.
        * **Design e Acessibilidade:** Em conformidade com as diretrizes teóricas da disciplina, o layout foi rigorosamente pautado por acessibilidade visual (empregando a paleta contínua sequencial *Viridis* e a paleta categórica de Okabe e Ito, perfeitamente seguras para daltônicos). Alinhado ao princípio do ***Data-Ink Ratio*** formulado por **Edward Tufte**, a interface utiliza o `Pandas Styler` e containers discretos para eliminar ruídos visuais (*chartjunk*) e garantir um alinhamento matricial preciso dos dados financeiros, maximizando a eficiência empírica na comunicação analítica.
        """)

st.write("")
st.caption("Desenvolvido para avaliação final do módulo de visualização de dados e métricas em ambientes interativos.")