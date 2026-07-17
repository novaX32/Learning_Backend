from fastapi import FastAPI,Query
from pydantic import BaseModel,Field,field_validator
from typing import Annotated,Literal,List,Optional
from datetime import datetime

app=FastAPI()

class FilterParams(BaseModel):
    model_config={"extra":"forbid"}
    limit:int=Field(50,gt=0,le=100,description="No ofitems to be return")
    offset:int=Field(0,ge=0,description="No of items to skip")
    order_by:Literal["created_at","updated_at","price"]=Field("created_at",description="field to sort by")
    order:Literal["asc","desc"]=Field("desc",description="sorting direction")
    tags:List[str]=Field(default_factory=list,description="filter by tags")
    min_price:Optional[int]=Field(None,ge=0,description="Minimum Price")
    max_price:Optional[int]=Field(None,description="Maximum price")
    is_active:Optional[bool]=Field(None,description="filter activate items only")

    @field_validator("max_price")
    @classmethod
    def validate_price_range(cls,v,info):
        if v is not None and info.data.get("min_price") is not None:
            if v<info.data["min_price"]:
                raise ValueError("max_price must be greater than or equal to min_price")
        return v
    

class Item(BaseModel):
    id:int
    name:str
    price:float
    tags:List[str]
    is_active:bool
    created_at:datetime
    updated_at:datetime

class ItemResponse(BaseModel):
    items:List[Item]
    total:int
    limit:int
    offset:int


fake_items_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "tags": ["electronics", "tech"], "is_active": True, "created_at": datetime(2025, 1, 10), "updated_at": datetime(2025, 6, 1)},
    {"id": 2, "name": "Headphones", "price": 79.99, "tags": ["electronics", "audio"], "is_active": True, "created_at": datetime(2025, 2, 15), "updated_at": datetime(2025, 5, 20)},
    {"id": 3, "name": "Book", "price": 19.99, "tags": ["books"], "is_active": False, "created_at": datetime(2024, 12, 1), "updated_at": datetime(2025, 3, 10)},
    # ... add more items
]


@app.get("/")
def root():
    return{"message":"Query-Parameter-Models"}



@app.get("/items/",response_model=ItemResponse)
def read_items(filter_query:Annotated[FilterParams,Query()]):
    filtered=fake_items_db.copy()
    if filter_query.tags:
        filtered=[
            item
            for item in filtered
            if any (tag in item["tags"]for tag in filter_query.tags)
        ]
    if filter_query.min_price is not None:
        filtered=[ item for item in filtered if item["price"]>=filter_query.min_price]

    if filter_query.max_price is not None:
        filtered=[item for item in filtered if item["price"]<=filter_query.max_price]
    
    if filter_query.is_active is not None:
        filtered=[item for item in filtered if item["is_active"]==filter_query.is_active]

    reverse=filter_query.order=="desc"
    filtered.sort(
        key=lambda x:x.get(filter_query.order_by,0),
        reverse=reverse
    )

    total=len(filtered)
    pagination=filtered[
        filter_query.offset:filter_query.offset+filter_query.limit
    ]

    return ItemResponse(
        items=[Item(**item) for item in pagination],
        total=total,
        limit=filter_query.limit,
        offset=filter_query.offset

    )




