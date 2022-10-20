import pandas as pd
from sklearn import ensemble
from sklearn.model_selection import train_test_split
import pickle

data = pd.read_csv('./data/data_model_all.csv')
df_code = pd.read_excel('./data/zipcode_be.xlsx')
data = data.rename({'Unnamed: 0': 'id'}, axis=1)

data['code'] = data['zip_code']
df_code['code']=df_code['code'].astype(int)
data['code']=data['code'].astype(int)
data = data.merge(df_code, on='code', how='left')
data = data.drop_duplicates(subset="id")
data = data.dropna()
def rem_outliers(df, column, zscore = 3):
    #calculate upper and lower limits
    upper_limit = df[column].mean() + zscore * df[column].std()
    lower_limit = df[column].mean() - zscore * df[column].std()
    #outliers removed
    normal_df = df[(df[column] < upper_limit) & (df[column] > lower_limit)]
    return normal_df
data['building_state'] = (data['building_state']).replace({'good': 0, 'to renovate': 0, 'as new': 1, 'to be done up': 0, 
'just renovated': 0, 'to restor':0, 'to rebuild':0 , 'not mentioned': 0})
labels = data['price']
df = rem_outliers(data, 'price')
df = df.drop(['id','full_address','name','province'],axis=1)

df_houses = df[df["property_type"].str.contains("house")]
df_apt = df[df["property_type"].str.contains("apartment")]
labels_houses =  df_houses['price']
labels_apt =  df_apt['price']
df_houses = df_houses.drop(["property_type", 'price'],axis=1)
df_apt = df_apt.drop(["property_type", 'price'],axis=1)


# X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.3,random_state=2)
# clf = ensemble.GradientBoostingRegressor(n_estimators=400,max_depth=6,min_samples_split=2,learning_rate=0.1,loss= 'squared_error')
# clf.fit(X_train,y_train)
# filename = './model/finalized_model.sav'
# pickle.dump(clf, open(filename, 'wb'))

def house_model(df_houses, labels_houses):
    X_train, X_test, y_train, y_test = train_test_split(df_houses, labels_houses, test_size = 0.3,random_state=2)
    clf_house = ensemble.GradientBoostingRegressor(n_estimators=400,max_depth=6,min_samples_split=2,learning_rate=0.1,loss= 'squared_error')
    clf_house.fit(X_train,y_train)
    print("im here--------------------------------")
    filename = './model/finalized_house_model.sav'
    pickle.dump(clf_house, open(filename, 'wb'))
    # score = clf_house.score(X_test,y_test)
    # pred = clf_house.predict(X_test)
    # print(f'the accuracy is {score}')
    # print(f'the prediction price is : {pred}')

def apt_model(df_apt, labels_apt):
    print("im here--------------------------------")
    X_train, X_test, y_train, y_test = train_test_split(df_apt, labels_apt, test_size = 0.3,random_state=2)
    clf_apartment = ensemble.GradientBoostingRegressor(n_estimators=400,max_depth=6,min_samples_split=2,learning_rate=0.1,loss= 'squared_error')
    clf_apartment.fit(X_train,y_train)
    filename = './model/finalized_apartment_model.sav'
    pickle.dump(clf_apartment, open(filename, 'wb'))
    score = clf_apartment.score(X_test,y_test)
    pred = clf_apartment.predict(X_test)
    print(f'the accuracy is {score}')
    print(f'the prediction price is : {pred}')

house_model(df_houses, labels_houses)
apt_model(df_apt, labels_apt)

# score = clf.score(X_test,y_test)
# house_data = {'area' :[423],'rooms_number' :[5],'zip_code' :[8500],'land_area':[2714],'garden':[1],'garden_area':[2291],'equipped_kitchen':[0],'swimming_pool':[0],'furnished':[0],'open_fire':[0],'terrace':[1],'terrace_area':[0],'facades_number':[4],'building_state':[1],'code':[8500],'lat':[508194894],'lng':[32577076]}
# test_df = pd.DataFrame(house_data)
# pred = clf.predict(X_test)
# print(f'the accuracy is {score}')
# print(f'the prediction price is : {pred}')