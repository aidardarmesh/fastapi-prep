import sys, time

from fastapi import FastAPI
from elasticsearch import Elasticsearch, exceptions


app = FastAPI()

es = Elasticsearch("http://localhost:9200")
ES_INDEX = "user_data"
# phone, id, first_name, last_name, gender
FB_PROFILE_URL = f"https://www.facebook.com/profile.php?id={id}"
FB_DATA_DIR = "./data/fb.txt"


def check_index(index: str, retry: int = 5):
    """connect to ES with retry"""
    if not retry:
        print("Out of retries: terminating")
        sys.exit(1)

    try:
        if not es.indices.exists(index=index):
            mappings = {
                "properties": {
                    "phone_number": {"type": "text"},
                    "first_name": {"type": "text"},
                    "second_name": {"type": "text"},
                    "gender": {"type": "text"},
                    "fb_id": {"type": "text"}
                }
            }
            es.indices.create(index=index, mappings=mappings)
    except exceptions.ConnectionError as e:
        print(f"Unable to connect to ES: {e}\nRetrying in 5 sec")
        time.sleep(5)
        check_index(index, retry - 1)


@app.on_event("startup")
def load_bulk_data():
    """loads bulk user data if connected to ES before application starts"""
    check_index(ES_INDEX)
    counter = 0
    with open(FB_DATA_DIR, 'r') as file:
        for line in file:
            bulk_data = line.split(':')
            es.index(
                index=ES_INDEX,
                id=counter,
                document={
                    "phone_number": bulk_data[0],
                    "fb_id": bulk_data[1],
                    "first_name": bulk_data[2],
                    "last_name": bulk_data[3],
                    "gender": bulk_data[4]
                }
            )
            counter += 1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
async def search(q: str):
    return es.search(
        index=ES_INDEX,
        body={
            "query": {
                "match": {
                    "phone_number": q
                }
            }
        }
    )
