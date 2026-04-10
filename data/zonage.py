import pandas as pd
from pathlib import Path

base_dir = Path(__file__).parent
file_path = base_dir / "liste_communes_zonage_sept_2025.xlsx"

df = pd.read_excel(file_path, dtype=str)

df = df[['LIBGEO', 'Zonage en vigueur depuis le 5 septembre 2025']]

df['LIBGEO'] = df['LIBGEO'].str.strip().str.upper()
df['Zonage en vigueur depuis le 5 septembre 2025'] = df['Zonage en vigueur depuis le 5 septembre 2025'].str.upper()

commune_to_zone = dict(zip(df['LIBGEO'], df['Zonage en vigueur depuis le 5 septembre 2025']))

print(df.head())