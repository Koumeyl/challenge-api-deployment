from enum import Enum
from typing import Optional
from fastapi import Body,FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from preprocessing.cleaning_data import preprocessing
from predict.prediction import prediction

class Property_type(str, Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    OTHERS = "OTHERS"


class Building_state(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    TO_RENOVATE = "TO RENOVATE"
    JUST_RENOVATED = "JUST RENOVATED"
    TO_REBUILD = "TO REBUILD"


class Data(BaseModel):
    area: int
    property_type: Property_type
    rooms_number: int
    zip_code: int
    land_area: Optional[int] | None = None
    garden: Optional[bool] | None = None
    garden_area: Optional[int] | None = None
    equipped_kitchen: Optional[bool] | None = None
    full_address: Optional[str] | None = None
    swimming_pool: Optional[bool] | None = None
    furnished: Optional[bool] | None = None
    open_fire: Optional[bool] | None = None
    terrace: Optional[bool] | None = None
    terrace_area: Optional[int] | None = None
    facades_number: Optional[int] | None = None
    building_state: Optional[
      Building_state]  | None = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Alive!"}

@app.post("/data/")
async def post_data(data: Data = Body(embed=True)):
    if data.area  == 0:
        raise HTTPException(status_code = 422, detail=  "area cannot be zero")   
    if data.rooms_number  == 0:
        raise HTTPException(status_code = 422, detail=  "rooms_number cannot be zero")   
    if data.zip_code  == 0:
        raise HTTPException(status_code = 422, detail=  "zip_code cannot be zero") 
    if data.property_type  == Property_type.OTHERS:
        raise HTTPException(status_code = 422, detail=  "Predictions for others are not supported")
    print("data: ", data)
    print("type: ",type(data))
    print("data.data: ", data.dict())
    print("type.data: ",type(data.dict()))
    df = pd.DataFrame.from_dict([data.dict()])
    df = preprocessing(df)
    print(f"preprocessed df------------------ {df.head()}")
    pred = prediction(df)
    prediction_dict = {"prediction" : pred[0]}
    return prediction_dict