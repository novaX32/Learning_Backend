from fastapi import FastAPI,Query
from typing import Annotated

app=FastAPI()


@app.get("/")
def root():
    return{"message":"Query Parameters and String Validations"}

@app.get("/items/")
def read_item(q:Annotated[list[str]|None,Query(alias="item-query",title="Query string",description="search term for item...",deprecated=True,include_in_schema=False)]=["foo","bar"]):
    result={"items":[{"item_id":"foo"},{"item_id":"bar"}]}
    if q:
        result.update({"q":q})
    return result