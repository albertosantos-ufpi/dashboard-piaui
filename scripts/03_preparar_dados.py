from pathlib import Path
import re
import unicodedata

import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
PROCESSADOS = RAIZ / "data" / "processed"

PROCESSADOS.mkdir(parents=True, exist_ok=True)


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )
    return texto.lower().strip()


def identificar_dimensao(df, descricao):
    cabecalho = df.iloc[0]

    for coluna in df.columns:
        if not re.fullmatch(r"D\d+N", coluna):
            continue

        if normalizar(cabecalho[coluna]) == descricao:
            prefixo = coluna[:-1]
            return prefixo + "C", coluna

    raise ValueError(
        f"Dimensão '{descricao}' não identificada. "
        f"Cabeçalho recebido: {cabecalho.to_dict()}"
    )


def carregar_sidra(caminho):
    df = pd.read_csv(
        caminho,
        dtype=str,
        encoding="utf-8-sig"
    )

    if df.empty:
        raise ValueError(f"Arquivo vazio: {caminho.name}")

    municipio_codigo, municipio_nome = identificar_dimensao(
        df, "municipio"
    )
    variavel_codigo, variavel_nome = identificar_dimensao(
        df, "variavel"
    )
    ano_codigo, _ = identificar_dimensao(df, "ano")

    dados = df.iloc[1:].copy()

    dados = dados[
        dados["NC"].eq("6")
        & dados[municipio_codigo].str.fullmatch(
            r"22\d{5}", na=False
        )
    ].copy()

    resultado = pd.DataFrame({
        "cod_municipio": dados[municipio_codigo],
        "municipio": (
            dados[municipio_nome]
            .str.replace(r"\s*-\s*PI$", "", regex=True)
            .str.strip()
        ),
        "cod_variavel": dados[variavel_codigo].astype(str).str.strip(), # Remove espaços invisíveis
        "variavel": dados[variavel_nome],
        "ano": dados[ano_codigo],
        "unidade": dados["MN"],
        "valor": pd.to_numeric(dados["V"], errors="coerce")
    })
    
    if resultado.empty:
        raise ValueError(
            f"Nenhum município do Piauí encontrado em {caminho.name}."
        )

    return resultado


# Carrega os dados brutos
pib = carregar_sidra(RAW / "pib_piaui.csv")
pop = carregar_sidra(RAW / "populacao_piaui.csv")

# Carrega os dados brutos
pib = carregar_sidra(RAW / "pib_piaui.csv")
pop = carregar_sidra(RAW / "populacao_piaui.csv")

# --- NOVO BLOCO DE PROTEÇÃO CONTRA ANOS PRELIMINARES INCOMPLETOS ---
# 1. Joga fora as linhas onde o IBGE ainda não divulgou o valor (NaN)
pib = pib.dropna(subset=["valor"])
pop = pop.dropna(subset=["valor"])

# 2. Ordena do ano mais novo para o mais velho e mantém apenas o 1º registro válido de cada variável
pib = pib.sort_values("ano", ascending=False).drop_duplicates(subset=["cod_municipio", "cod_variavel"])
pop = pop.sort_values("ano", ascending=False).drop_duplicates(subset=["cod_municipio", "cod_variavel"])
# -------------------------------------------------------------------


# ---------------------------------------------------------
# 1. PROCESSAMENTO DA BASE PRINCIPAL
# ---------------------------------------------------------
pib_total = pib[pib["cod_variavel"].eq("37")].copy()
populacao = pop[pop["cod_variavel"].eq("9324")].copy()

unidades_pib = set(pib_total["unidade"].map(normalizar))
if unidades_pib == {"mil reais"}:
    pib_total["valor"] = pib_total["valor"] * 1000

base = populacao[
    ["cod_municipio", "municipio", "valor", "ano"]
].rename(columns={
    "valor": "populacao",
    "ano": "ano_populacao"
})

base = base.merge(
    pib_total[["cod_municipio", "valor", "ano"]].rename(
        columns={
            "valor": "pib_total",
            "ano": "ano_pib"
        }
    ),
    on="cod_municipio",
    how="left",
    validate="one_to_one"
)

# Calcula o PIB per capita
base["pib_per_capita"] = base["pib_total"] / base["populacao"]
base = base.sort_values("municipio").reset_index(drop=True)

base.to_parquet(
    PROCESSADOS / "base_piaui.parquet",
    index=False
)

# ---------------------------------------------------------
# 2. PROCESSAMENTO DOS SETORES ECONÔMICOS
# ---------------------------------------------------------
codigos_setores = {
    "513": "Agropecuária",
    "517": "Indústria",
    "6575": "Serviços",
    "525": "Administração Pública"
}

# Remove qualquer sujeira da string e seleciona apenas os setores desejados
pib["cod_variavel_str"] = pib["cod_variavel"].astype(str).str.strip()
setores = pib[pib["cod_variavel_str"].isin(codigos_setores.keys())].copy()

# Mapeia os nomes amigáveis
setores["setor"] = setores["cod_variavel_str"].map(codigos_setores)

# TRUQUE DE MESTRE AQUI: A coluna original pode vir com vírgulas ou o string '-' 
# Convertendo forçadamente e substituindo os inválidos por 0
setores["valor_numerico"] = pd.to_numeric(setores["valor"], errors="coerce").fillna(0)

# Multiplica por 1.000 (porque a unidade do IBGE é "Mil Reais")
setores["valor"] = setores["valor_numerico"] * 1000

# Seleciona apenas as 3 colunas que vão para o parquet
setores = setores[["cod_municipio", "setor", "valor"]]

# Salva o arquivo final
setores.to_parquet(
    PROCESSADOS / "setores_piaui.parquet",
    index=False
)

# DIAGNÓSTICO (deve mostrar valores em Reais absurdamente altos, e não 0.0)
print("\n--- DIAGNÓSTICO DOS SETORES ---")
print(f"Linhas salvas: {len(setores)} (Esperado: 896)")
print("Soma por setor (em R$):")
print(setores.groupby("setor")["valor"].sum())