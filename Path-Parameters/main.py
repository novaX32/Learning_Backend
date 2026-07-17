from fastapi import FastAPI
from enum import Enum

app=FastAPI()



class ModelName(str,Enum):
    admin="admin"
    user="user"
    hacker="hacker"

@app.get("/")
def root():
    return{"Message":"Path Parameter"}

@app.get("/items/{item_id}")
def get_item(item_id:int):
    return{"message":item_id}




@app.get("/users/me")
def get_user():
    return{"message":"me"}




@app.get("/users/{user_type}")
def get_user(user_type:ModelName):
    if user_type is ModelName.admin:
        return {"message":"User is admin"}
    elif user_type is ModelName.user:
        return {"message":"User is user"}
    else:
        return {"message":"User is hacker"}
    
@app.get("/users/{user_type}")
def get_user(user_type):
    return{"message":user_type}
    






