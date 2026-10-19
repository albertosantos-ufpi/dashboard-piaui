import geopandas as gpd

gdf = gpd.read_file("data/raw/BR_Municipios_2022.shp")

piaui = gdf[gdf["CD_MUN"].str.startswith("22")].copy()
piaui = piaui[["CD_MUN", "NM_MUN", "geometry"]]
piaui = piaui.rename(columns={
    "CD_MUN": "cod_municipio",
    "NM_MUN": "municipio"
})

piaui.to_file("data/geo/piaui_municipios.geojson", driver="GeoJSON")

print(f"Municípios exportados: {len(piaui)}")