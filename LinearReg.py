import pandas as pd
import matplotlib.pyplot as plt
#matplotlib inlinefrom
import xlrd
from sklearn.linear_model import LinearRegression
import seaborn as sns

x_df = []
y_df = []
y_test = []
tel = 0

#df = pd.read_excel('F:\\Energie\\buffervat-dec-2021-geleverd.csv')
df = pd.read_excel('F:\\Energie\\test1.xlsx')
print(df.info())
df.head()
df_zonder = df.dropna()
print(df_zonder.isnull().sum())
print(df_zonder.shape)
correlaties = df_zonder.corr()
sns.heatmap(correlaties)
df_zonder.info()

elec_dummy = pd.get_dummies(df_zonder['ElecPlan'])
elec_dummy.head()

df_zonder_dummy = df_zonder.drop(['Tijd', 'ElecPlan'], axis = 1)
df_voor_ml = pd.concat([df_zonder_dummy, tijd_dummy, elecplan_dummy], axis = 1)
y = df_voor_ml['ElecWerkelijk']
X = df_voor_ml.drop('ElecWerkelijk', axis = 1)

# df = pd.get_dummies(df, columns=['Tijd', 'ElecPlan', 'ElecWerkelijk'])
#
# for row in df:
#
#     print(row[0])
#     print(row[1])
#     #x_df.append(row[0])
#     #y_df.append(row[1])
#
#     tel = tel + 1
#     if tel >= 20:
#         break
#
#
# y = df['ElecWerkelijk']
# X = df.drop(['Tijd', 'ElecPlan', 'ElecWerkelijk'], axis=1)
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# model = LinearRegression()model.fit(X_train, y_train)
# y_train_score = model.predict(X_train)y_test_score = model.predict(X_test)
#
# sns.pairplot(df, kind='reg')
# plt.show()