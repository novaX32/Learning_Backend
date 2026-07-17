from fastapi import FastAPI

app=FastAPI()


@app.get("/")
def root():
    return{"Message":"Query Parameter"}

list=[1,2,3,4,5,6,7,8,9,10]

@app.get("/items/")
def get_num(start:int=0,end:int=10):
    return{"List":list[start:start+end]}


long_text="The sun sets slowly behind the tall mountains. The sky turns into a bright mix of orange and pink. Birds fly back to their cozy nests. The cool evening breeze starts to blow through the green trees. People in the small town sit on their porches. They drink warm tea and share stories. The stars begin to twinkle in the dark night sky. It is a quiet and peaceful end to the long day."

short_text="The sun sets. The sky turns pink. Birds fly home. Cool breezes blow. The stars come out. It is a peaceful night."

@app.get("/items/{item_id}")
def get_text(text:bool=True):
    if text:
        return short_text
    else:
        return long_text