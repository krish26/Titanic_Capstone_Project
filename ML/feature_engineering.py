import pandas as pd
import numpy as np

# def engineer_features(df: pd.DataFrame):
    
#     # Title extraction from Name
#     df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

#     # Standardize some titles
#     df['Title'] = df['Title'].replace({
#         'Mlle': 'Miss',
#         'Ms': 'Miss',
#         'Mme': 'Mrs'
#     })

#     # Replace rare titles with 'Rare'
#     rare_titles = ["Lady","Countess","Capt","Col","Don","Dr","Major","Rev","Sir","Jonkheer","Dona"]
#     df['Title'] = df['Title'].replace(rare_titles, "Rare")

#     # Age binning to pdata_inspect notebook to manage missing values better and to maintain execution flow.
#     #     # df['AgeGroup'] = pd.cut(
#     #     df['Age'], bins=[0,12,18,35,60,100],
#     #     labels=['Child','Teen','YoungAdult','Adult','Senior']
#     # )

#     # Fare binning
    
#     #4 is fare is split into different quartlies
#     #<25% - low fares , 25%-50% - mid fares, 50%-75% - high fares, >75% - very high fares
    
#     df['FareGroup'] = pd.qcut(df['Fare'], 4, labels=['Low','Mid','High','VeryHigh'])

#     # Family features
#     df['FamilySize'] = df['SibSp'] + df['Parch'] + 1 #including self
#     df['IsAlone'] = (df['FamilySize']==1).astype(int) #1 if alone, 0 otherwise

#     return df

def extract_title(df: pd.DataFrame):
    # Extract Title from Name
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

    # Standardize equivalent titles
    df['Title'] = df['Title'].replace({
        'Mlle': 'Miss',
        'Ms': 'Miss',
        'Mme': 'Mrs'
    })

    # Group rare titles
    rare_titles = ["Lady","Countess","Capt","Col","Don","Dr","Major","Rev","Sir","Jonkheer","Dona"]
    df['Title'] = df['Title'].replace(rare_titles, "Rare")

    return df


def create_age_bins(df: pd.DataFrame):
    # Fill missing Age using median per Title
    df['Age'] = df.groupby('Title')['Age'].transform(
        lambda x: x.fillna(x.median())
    )

    # Just in case any Title group had all NaN
    df['Age'] = df['Age'].fillna(df['Age'].median())

    # Create AgeGroup
    df['AgeGroup'] = pd.cut(
        df['Age'],
        bins=[0,12,18,35,60,np.inf],
        labels=['Child','Teen','YoungAdult','Adult','Senior'],
        include_lowest=True
    )

    return df


def engineer_features(df: pd.DataFrame):
    df = extract_title(df)
    df = create_age_bins(df)

    # Fare binning
    df['FareGroup'] = pd.qcut(
        df['Fare'], 4,
        labels=['Low','Mid','High','VeryHigh']
    )

    # Family features
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

    return df


