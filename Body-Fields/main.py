from fastapi import FastAPI,Body
from pydantic import BaseModel,Field,field_validator,ValidationError
from typing import Annotated,List
from enum import Enum

app=FastAPI()



class Category(str,Enum):
    ELECTRONICS="electronics"
    CLOTHING="clothing"
    BOOKS="books"

class Image(BaseModel):
    url:str=Field(...,min_length=5,max_length=500)
    alt:str|None=Field(None,max_length=100)

class Item(BaseModel):
    name:str=Field(...,min_length=5,max_length=500)
    description:str|None=Field(default=None,
                               title="description of item",
                               max_length=300,
                               description="Item Description")
    price:float=Field(...,gt=0,le=100000)
    tax:float|None=Field(None,ge=0)
    category:Category=Field(...)
    tags:list[str]=Field(default_factory=list,max_length=10)
    images:list[Image]=Field(default_factory=list,max_length=5)
    discount_code: str | None = Field(
    None,
    pattern=r"^[A-Z0-9]{5,10}$",
    examples=["SUMMER25", "BLACKFRIDAY"]
    )
    discount: float | None = Field(
    None,
    ge=0,
    le=100
)
    @field_validator("name")
    @classmethod
    def name_must_be_proper(cls,v:str)->str:
        if len(v.strip())<3:
            raise ValueError("name must be atlist 3 char")
        return v.strip().title()
    @field_validator("discount")
    
    @classmethod
    def discount_must_be_reasonable(cls,v:float|None,info)->float|None:
        if v is not None and v>50:
            price=info.data.get('price')
            if price is not None and price<100:
                raise ValueError("high descounts are not allowed")
        return v
    

@app.put("/items/{item_id}")
def update_item(item_id:int,item:Annotated[Item,Body(embed=True)]):
    item=item.model_dump()
    item["item_id"]=item_id
    return item

@app.post("/items/{item_id}")
def create_item(item_id:int,item:Annotated[Item,Body(embed=True)]):
    item=item.model_dump()
    item["item-id"]=item_id
    return{"Message":"Item created","item":item}