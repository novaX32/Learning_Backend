from fastapi import FastAPI,Path,Query
from typing import Annotated
from pydantic import BaseModel,Field


app=FastAPI()

items = [
    {"item_id": 1, "name": "Laptop", "price": 55000},
    {"item_id": 2, "name": "Mouse", "price": 500},
    {"item_id": 3, "name": "Keyboard", "price": 1200},
    {"item_id": 4, "name": "Monitor", "price": 12000},
    {"item_id": 5, "name": "Headphones", "price": 2500},
    {"item_id": 6, "name": "Webcam", "price": 3000},
    {"item_id": 7, "name": "USB Drive", "price": 800},
    {"item_id": 8, "name": "External HDD", "price": 4500},
    {"item_id": 9, "name": "SSD", "price": 6000},
    {"item_id": 10, "name": "Printer", "price": 9000},
    {"item_id": 11, "name": "Scanner", "price": 7000},
    {"item_id": 12, "name": "Tablet", "price": 22000},
    {"item_id": 13, "name": "Smartphone", "price": 35000},
    {"item_id": 14, "name": "Smartwatch", "price": 15000},
    {"item_id": 15, "name": "Camera", "price": 50000},
    {"item_id": 16, "name": "Speaker", "price": 4000},
    {"item_id": 17, "name": "Microphone", "price": 3500},
    {"item_id": 18, "name": "Router", "price": 2800},
    {"item_id": 19, "name": "Projector", "price": 30000},
    {"item_id": 20, "name": "Power Bank", "price": 1800},
    {"item_id": 21, "name": "Charger", "price": 1200},
    {"item_id": 22, "name": "Cable", "price": 300},
    {"item_id": 23, "name": "Graphics Card", "price": 45000},
    {"item_id": 24, "name": "Processor", "price": 25000},
    {"item_id": 25, "name": "RAM", "price": 8000},
    {"item_id": 26, "name": "Motherboard", "price": 15000},
    {"item_id": 27, "name": "Cabinet", "price": 5000},
    {"item_id": 28, "name": "Cooling Fan", "price": 1200},
    {"item_id": 29, "name": "UPS", "price": 6500},
    {"item_id": 30, "name": "Network Switch", "price": 8500},
]

class ItemQuery(BaseModel):
    q:str|None=Field(
        default=None,
        alias="search",
        min_length=2,
        max_length=1000,
        description="Search Item"
    )
    size:float|None=Field(
        default=None,
        gt=0,
        lt=100,
        description="Size in cm"
    )
@app.get("/")
def root():
    return {"message":"Path-Parameters-and-Numeric-Validations"}

@app.get("/items/{item_id}/{category}")
def read_item(
 item_id:Annotated[int,Path(gt=1,le=1000)],
 category:Annotated[str,Path(min_length=3,max_length=20)],
 query:Annotated[ItemQuery,Query()]
):
     return {
     "item_id": item_id,
        "category": category,
        "search": query.q,
        "size": query.size
 }

@app.get("/users/{user_id}")
def get_user(user_id:Annotated[int,Path(title="get user")]):
    return{"user_id":user_id}

@app.get("/product/{product_id}")

def get_product(
    product_id:
        Annotated[int,
                  Path(
                      ge=1,
                      le=100000,
                      title="product id",description="search for a product")],
    currency:
        Annotated[
            str|None , 
            Query(
                alias="c")]=None  
            ):
    
    return{"product_id":product_id,"currency":currency}

@app.get("/account/{account_id}/balance")
def get_balance(account_id:Annotated[int,Path(ge=0)],
                min_balance:Annotated[int|None,Query(ge=0,alias="min_balance")]):
    result={
        "account_id":account_id,

    }
    if min_balance:
        result["min_balance"]=min_balance
    return result

@app.get("/blog/{blog_slug}")
def get_blog(blog_slug:Annotated[str,Path(min_length=5,max_length=50)]):
    return{"blog_slug":blog_slug}

@app.get("/restaurants/{restaurant_id}/menu")
def get_food(restaurant_id:Annotated[int,Path(ge=0)],
             min_rating:Annotated[float|None,Query(ge=1,le=5)]=None,
             category:Annotated[str|None,Query()]=None):
    result={
        "restaurant_id":restaurant_id,
        "min_rating":5.0,
        "category":"xyz"
    }
    if min_rating:
        result["min_rating"]=min_rating
    if category:
        result["category"]=category
    return result


@app.get("/users/{user_id}/posts")
def get_user(user_id:Annotated[int,Path(ge=0)],
            limit:Annotated[int,Query(ge=1,le=100)],
             offset:Annotated[int,Query(ge=0)] ):
    return "hii"


@app.get("/product/{item_id}/{category}")
def get_product(
    item_id: Annotated[int, Path(ge=1, le=30)],
    category: Annotated[str, Path(min_length=3)],
    sort: Annotated[str | None, Query()] = None,
    limit: Annotated[int | None, Query(ge=1, le=10)] = None,
    offset: Annotated[int | None, Query(ge=0, le=30)] = None,
):
    offset = offset or 0
    limit = limit or len(items)

    result = items[offset:offset + limit]

    if sort and sort in result[0]:
        result.sort(key=lambda item: item[sort])

    return {"items": result}

    