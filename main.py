from fastapi import FastAPI
from elasticsearch import Elasticsearch
from pydantic import BaseModel


app = FastAPI()

es = Elasticsearch("http://localhost:9200")
# phone, id, first_name, last_name, gender
FB_PROFILE_URL = f"https://www.facebook.com/profile.php?id={id}"


class SearchQuery(BaseModel):
    query: str


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
