import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_DIR / "data"

def load_cleaned() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / 'viscoelastic_cleaned.csv', keep_default_na=False, na_values='')

def save_features(df: pd.DataFrame, name: str) -> None:
    df.to_csv(DATA_DIR / f'{name}.csv', index=False)

def drop_rheological(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[
        'g_0',
        'g_min',
        'omega_cr',
        'tau_r',
        'eta_0'
    ])

def drop_ids(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[
        'id_surfactant1',
        'id_surfactant2',
        'id_additive1',
        'id_additive2'
    ])

def drop_smiles(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[
        'smiles_surfactant1',
        'smiles_surfactant2',
        'smiles_additive1',
        'smiles_additive2'
    ])

def add_expert_chen(df: pd.DataFrame, columns, na=np.nan):
    expert_chen = pd.read_csv(DATA_DIR / 'expert_chen.csv', keep_default_na=False, na_values='')
    expert_chen.loc[len(expert_chen)] = ['None'].extend(np.ones(18) * na)
    expert_chen = expert_chen.set_index('smiles')
    for column in columns:
        prefix = column.replace('smiles_','')
        df = df.merge(expert_chen.add_prefix(prefix + '_'), left_on=column, right_on='smiles', how='left')
    return df

def add_physiochemical(df: pd.DataFrame, columns, na=np.nan):
    physiochemical = pd.read_csv(DATA_DIR / 'physiochemical.csv', keep_default_na=False, na_values='')
    physiochemical.loc[len(physiochemical)] = ['None'].extend(np.ones(256) * na)
    physiochemical = physiochemical.set_index('smiles')
    for column in columns:
        prefix = column.replace('smiles_','')
        df = df.merge(physiochemical.add_prefix(prefix + '_'), left_on=column, right_on='smiles', how='left')
    return df