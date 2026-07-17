from fastapi import FastAPI,Path,Body
from typing import Annotated
from pydantic import BaseModel,EmailStr

app=FastAPI()
class Item(BaseModel):
    name:str
    description:str|None=None
    price:float
    tax:float|None=None

class User(BaseModel):
    name:str
    email:EmailStr

class Item_Response(BaseModel):
    item_id:int
    important:bool|None=None
    q:str|None=None
    item:Item|None=None
    user:User|None=None



@app.get("/")
def root():
    return{"message":"Mixing-Path-Query-and-BodyParameters"}

@app.put("/items/{item_id}",response_model=Item_Response)
def update_item(*,item_id:Annotated[int,Path(description="id of an item")],
                important:Annotated[bool|None,Body()]=None,
                q:str|None=None,
                item:Item|None=None,
                user:User|None=None,
                ):
    result={"item_id":item_id,"important":important}
    if q:
        result.update({"q":q})
    if item:
        result.update({"item":item})
    if user:
        result.update({"user":user})

    return result




