import pickle
import pandas as pd
import enum as Enum
pickled_model_house =pickle.load(open('./model/finalized_house_model.sav', 'rb'))
pickled_model_apartment = pickle.load(open('./model/finalized_apartment_model.sav', 'rb'))
def prediction(df):
    print("predict df:",df)
    if "HOUSE" in df["property_type"].values:
        pickled_model = pickled_model_house
    if "APARTMENT" in df["property_type"].values:
        pickled_model = pickled_model_apartment



    df_code = pd.read_excel('./data/zipcode_be.xlsx')
    df['code'] = df['zip_code']
    df['code']=df['code'].astype(int)
    df = df.merge(df_code, on='code', how='left')
    print("----------------------------------------------------------------",df.head())
    pred = pickled_model.predict(df.drop(['full_address','property_type', 'name', 'province'], axis=1))
    print(f'the prediction price is : {pred}')
    return pred