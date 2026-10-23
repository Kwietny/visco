import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from modules.data_loader import drop_ids, drop_smiles, add_physiochemical, drop_rheological, load_cleaned, add_expert_chen


def quick_load(feature, columns):
    df = load_cleaned()
    df = drop_rheological(df)
    if feature == 'expert_chen':
        df = add_expert_chen(df, columns=columns)
    elif feature == 'physiochemical':
        df = add_physiochemical(df, columns=columns)
    else:
        return None
    df = drop_smiles(df)
    return df

def xy_split(df):
    y = df['viscoelasticity']
    X = df.drop(columns=['viscoelasticity'])
    X = drop_ids(X)
    groups = df[['id_surfactant1', 'id_surfactant2', 'id_additive1', 'id_additive2']].fillna('NONE').apply(tuple, axis=1)
    return X, y, groups

def simple_test(classifier, X, y, groups, plot=True):
    cv = StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)

    categorical_features = ['type_surfactant1', 'type_surfactant2']
    numerical_features = []

    for column in X.columns:
        if X[column].dtype in ('float64', 'int64'):
            numerical_features.append(column)

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    y_proba = cross_val_predict(model, X, y, groups=groups, cv=cv, method='predict_proba')[:, 1]
    fpr, tpr, thresholds = roc_curve(y, y_proba)
    roc_auc = auc(fpr, tpr)

    if plot:
        plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.3f})")
        plt.plot([0, 1], [0, 1], "k--", label="Random classifier")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.legend()
        plt.show()

    return roc_auc

def serial_test(classifier, X, y, groups):
    cv = StratifiedGroupKFold(n_splits=10, shuffle=True)

    categorical_features = ['type_surfactant1', 'type_surfactant2']
    numerical_features = []

    for column in X.columns:
        if X[column].dtype in ('float64', 'int64'):
            numerical_features.append(column)

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    aucs = []
    for _ in range(10):
        y_proba = cross_val_predict(model, X, y, groups=groups, cv=cv, method='predict_proba')[:, 1]
        fpr, tpr, thresholds = roc_curve(y, y_proba)
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        print(f"AUC: {roc_auc:.3f}")

    mean_auc = np.mean(aucs)
    std_auc = np.std(aucs, ddof=1)
    print(f"Mean: {mean_auc:.4f}")
    print(f"Std:   {std_auc:.4f}")