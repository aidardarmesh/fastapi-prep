from fastapi import FastAPI
from elasticsearch import Elasticsearch
from pydantic import BaseModel


app = FastAPI()

es = Elasticsearch(host="es")
# phone, id, first_name, last_name, gender
FB_PROFILE_URL = f"https://www.facebook.com/profile.php?id={id}"
FB_DATA_DIR = "./data/fb.txt"


class SearchQuery(BaseModel):
    query: str


@app.on_event("startup")
async def load_bulk_data():
    # create es index
    with open(FB_DATA_DIR, 'r') as file:
        for line in file:
            bulk_data = line.split(':')
            # put bulk data
            # try to use batch processing


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/search")
async def search(q: SearchQuery):
    return es.search(
        index="first_index",
        body={
            "query": {
                "match": {
                    "phone_number": q.query
                }
            }
        }
    )
