import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

symptoms_dataset = pd.read_csv('symptoms_dataset.csv')

df = symptoms_dataset.copy()
target = 'infectionProb'
encode = ['bodyPain', 'runnyNose', 'diffBreath']

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]


target_mapper = {'NO': 0, 'YES': 1}


def target_encode(val):
    return target_mapper[val]


df['infectionProb'] = df['infectionProb'].apply(target_encode)

# Separating X and y
X = df.drop('infectionProb', axis=1)
Y = df['infectionProb']

# Build random forest model
clf = RandomForestClassifier()
clf.fit(X, Y)

# Saving the model
pickle.dump(clf, open('symptoms_clf.pkl', 'wb'))
