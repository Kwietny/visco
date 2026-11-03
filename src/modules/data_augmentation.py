import pandas as pd
import numpy as np

def augment(df):
    swapped_surf = df.copy()
    swapped_surf[[
        'id_surfactant1',
        'type_surfactant1',
        'smiles_surfactant1',
        'c_surfactant1',
        'id_surfactant2',
        'type_surfactant2',
        'smiles_surfactant2',
        'c_surfactant2',
    ]] = swapped_surf[[
        'id_surfactant2',
        'type_surfactant2',
        'smiles_surfactant2',
        'c_surfactant2',
        'id_surfactant1',
        'type_surfactant1',
        'smiles_surfactant1',
        'c_surfactant1',
    ]]
    swapped_addi = df.copy()
    swapped_addi[[
        'id_additive1',
        'smiles_additive1',
        'c_additive1',
        'id_additive2',
        'smiles_additive2',
        'c_additive2',
    ]] = swapped_addi[[
        'id_additive2',
        'smiles_additive2',
        'c_additive2',
        'id_additive1',
        'smiles_additive1',
        'c_additive1',
    ]]
    swapped_both =df.copy()
    swapped_both[[
        'id_surfactant1',
        'type_surfactant1',
        'smiles_surfactant1',
        'c_surfactant1',
        'id_surfactant2',
        'type_surfactant2',
        'smiles_surfactant2',
        'c_surfactant2',
        'id_additive1',
        'smiles_additive1',
        'c_additive1',
        'id_additive2',
        'smiles_additive2',
        'c_additive2',
    ]] = swapped_both[[
        'id_surfactant2',
        'type_surfactant2',
        'smiles_surfactant2',
        'c_surfactant2',
        'id_surfactant1',
        'type_surfactant1',
        'smiles_surfactant1',
        'c_surfactant1',
        'id_additive2',
        'smiles_additive2',
        'c_additive2',
        'id_additive1',
        'smiles_additive1',
        'c_additive1',
    ]]
    augmented = pd.concat([df.copy(), swapped_surf, swapped_addi, swapped_both], ignore_index=True)
    return augmented

def augemnted_groupping(row):
    group = [row['id_surfactant1'], row['id_surfactant2'], row['id_additive1'], row['id_additive2']]
    group.sort()
    return tuple(group)