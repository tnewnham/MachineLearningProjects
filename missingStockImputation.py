# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split


n = int(input())
dates = []
levels = []
for i in range(n):
    a, b = input().strip().split('\t')
    dates.append(a)
    try:
        levels.append(float(b))
    except:
        levels.append(np.nan)
        pass

dates_float = []
for x in dates:
     float_days = datetime.strptime(x, '%m/%d/%Y %H:%M:%S')
     dates_float.append(float_days)

#print(dates_float)

df = pd.Series(levels, index = dates_float)
df.index.name = 'date'

#print(df)
df = df.reset_index(name = 'levels')

df['date_delta'] = (df['date'] - df['date'].min())  / np.timedelta64(1,'D')

#print(df)

nullLevels = (df[df['levels'].isnull()]['date_delta'].values)

nullLevels = [[x] for x in nullLevels]
nullLevelsArray = np.asarray(nullLevels)

df = df.dropna()

dates, levels = [[x] for x in df['date_delta'].values], [[x] for x in df['levels'].values]

x_train, x_test, y_train, y_test = train_test_split(dates, levels, test_size=0.05, shuffle=False)
x_train, y_train = np.asarray(x_train), np.asarray(y_train)
x_test, y_test = np.asarray(x_test), np.asarray(y_test)

mdl = ExtraTreesRegressor(n_estimators=1000, n_jobs=-1, random_state=0)
mdl.fit(x_train, y_train)

y_pred = mdl.predict(nullLevelsArray)
for pred in y_pred:
    print("%0.2f" % (pred))