import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) :
    # Age binning
  
    df['AgeGroup'] = pd.cut(
        df['Age'], bins=[0,12,18,35,60,100],
        labels=['Child','Teen','YoungAdult','Adult','Senior']
    )

    # Fare binning
    
    df['FareGroup'] = pd.qcut(df['Fare'], 4, labels=['Low','Mid','High','VeryHigh'])

    # Family features
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize']==1).astype(int)

    return df
