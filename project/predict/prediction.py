import pickle
import pandas as pd

def prediction(df):
    print("predict df:", df)
    pickled_model = pickle.load(open('./model/finalized_model.sav', 'rb'))
    df_code = pd.read_excel('./data/zipcode_be.xlsx')
    df['code'] = df['zip_code']
    df['code']=df['code'].astype(int)
    df = df.merge(df_code, on='code', how='left')
    print("----------------------------------------------------------------",df.head())
    pred = pickled_model.predict(df.drop(['full_address','property_type', 'name', 'province'], axis=1))
    print(f'the prediction price is : {pred}')
    return pred