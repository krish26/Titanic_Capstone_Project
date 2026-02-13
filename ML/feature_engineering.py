import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame):
    # Title extraction from Name
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

    # Standardize some titles
    df['Title'] = df['Title'].replace({
        'Mlle': 'Miss',
        'Ms': 'Miss',
        'Mme': 'Mrs'
    })

    # Replace rare titles with 'Rare'
    rare_titles = ["Lady","Countess","Capt","Col","Don","Dr","Major","Rev","Sir","Jonkheer","Dona"]
    df['Title'] = df['Title'].replace(rare_titles, "Rare")

    # Age binning
    df['AgeGroup'] = pd.cut(
        df['Age'], bins=[0,12,18,35,60,100],
        labels=['Child','Teen','YoungAdult','Adult','Senior']
    )

    # Fare binning
    
    #4 is fare is split into different quartlies
    #<25% - low fares , 25%-50% - mid fares, 50%-75% - high fares, >75% - very high fares
    
    df['FareGroup'] = pd.qcut(df['Fare'], 4, labels=['Low','Mid','High','VeryHigh'])

    # Family features
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1 #including self
    df['IsAlone'] = (df['FamilySize']==1).astype(int) #1 if alone, 0 otherwise

    return df
