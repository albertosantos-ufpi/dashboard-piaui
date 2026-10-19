import requests
import pandas as pd

BASE = "https://apisidra.ibge.gov.br/values"


def consultar(url: str) -> pd.DataFrame:
    resposta = requests.get(url, timeout=180)

    if not resposta.ok:
        print("URL consultada:", resposta.url)
        print("Status:", resposta.status_code)
        print("Resposta da API:", resposta.text[:1000])
        resposta.raise_for_status()

    return pd.DataFrame(resposta.json())


# PIB municipal — todas as variáveis disponíveis da tabela 5938
url_pib = (
    f"{BASE}/t/5938/"
    "n6/in%20n3%2022/"
    "v/allxp/"
    "p/last%203"  # <-- MUDANÇA AQUI: Traz os últimos 3 anos em vez de apenas 1
)

# População residente estimada — tabela 6579
url_pop = (
    f"{BASE}/t/6579/"
    "n6/in%20n3%2022/"
    "v/9324/"
    "p/last"
)

print("Baixando dados de PIB municipal...")
df_pib = consultar(url_pib)

print("Baixando dados de população...")
df_pop = consultar(url_pop)

df_pib.to_csv(
    "data/raw/pib_piaui.csv",
    index=False,
    encoding="utf-8-sig"
)

df_pop.to_csv(
    "data/raw/populacao_piaui.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"PIB: {df_pib.shape[0]} linhas salvas em data/raw/pib_piaui.csv")
print(f"População: {df_pop.shape[0]} linhas salvas em data/raw/populacao_piaui.csv")