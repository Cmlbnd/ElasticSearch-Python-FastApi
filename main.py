from fastapi import FastAPI, Header
from pydantic import BaseModel
from elasticsearch import Elasticsearch
import uuid
import json

app = FastAPI()

class Text(BaseModel):
    text: str

async def generateUUID():
	return uuid.uuid1()

#POST to create new data
@app.post("/create")
async def createData(body: Text):
    uid = await generateUUID()

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    res = es.index(index="test-index", id=uid, body={"text": body.text})
    es.indices.refresh(index="test-index")

    return(uid)

#DELETE data in elasticSearch
@app.delete("/delete/{text_id}")
async def deleteData(text_id: str):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    res = es.delete(index="test-index", id=text_id)
    es.indices.refresh(index="test-index")

#GET all data stored
@app.get("/all")
def getData():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.refresh(index="test-index")
    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    return res

#GET specific data using 
@app.get("/{text_id}")
def getDataFromId(text_id: str):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.refresh(index="test-index")
    res = es.search(index="test-index", body={'query':{'match':{'_id':text_id}}})
    return res

#GET with Header, similar to google
@app.get("/search/{textToSearch}")
def searchData(textToSearch: str):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    res= es.search(index='test-index',body={
        'query':{
            'match':{
                "text": textToSearch
            }
        }
    })

    resultList = {};
    i = 0
    for hit in res['hits']['hits']:
        resultList[str(i)] = hit['_source']['text']
        i += 1
    return resultList #Result by default order to the best match first