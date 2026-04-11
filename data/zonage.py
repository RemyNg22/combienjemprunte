import pandas as pd
from pathlib import Path
from functools import lru_cache

base_dir = Path(__file__).parent
file_path = base_dir / "liste_communes_zonage_sept_2025.xlsx"


@lru_cache(maxsize=1)
def load_zonage():
    df = pd.read_excel(file_path, dtype=str)
    df = df[['LIBGEO', 'Zonage en vigueur depuis le 5 septembre 2025']]

    df['LIBGEO'] = df['LIBGEO'].str.strip().str.upper()
    df['Zonage en vigueur depuis le 5 septembre 2025'] = df[
        'Zonage en vigueur depuis le 5 septembre 2025'
    ].str.upper()

    return dict(zip(
        df['LIBGEO'],
        df['Zonage en vigueur depuis le 5 septembre 2025']
    ))


def get_zone_from_commune(commune: str) -> str | None:
    """
    Retourne la zone PTZ (A, B1, B2, C) selon la commune
    """
    if not commune:
        return None

    return load_zonage().get(commune.strip().upper())