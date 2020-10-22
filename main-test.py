from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

#Helper
def generateUID(text):
	return client.post("/create", json={"text": text})

def deleteAfterTest(uid):
	return client.delete("/delete/" + uid.json())

#Tests
def test_createData():
    uid = generateUID("this is a long text")
    assert uid.status_code == 200

    response = client.get("/" + uid.json())
    assert response.json()["hits"]["hits"][0]["_source"] == {"text": "this is a long text"}
    deleteAfterTest(uid)

def test_deleteData():
    uid = generateUID("this is a long text")
    response = client.delete("/delete/" + uid.json())
    assert response.status_code == 200

    response =  client.get("/" + uid.json())  
    assert response.json()["hits"]["hits"] == []

def test_getDataFromNotExistingId():
    response = client.get("/notAnId")
    assert response.status_code == 200
    assert response.json()["hits"]["hits"] == []

def test_searchData():
    uid1 = generateUID("My test is running")
    uid2 = generateUID("Test succeed")
    uid3 = generateUID("Test successful")
    uid4 = generateUID("Application to squirro")
    searchResultBody = {
    '0': 'Test succeed',
    '1': 'Test successful',
    '2': 'My test is running'}

    response = client.get("/search/test+success")
    assert response.status_code == 200
    assert response.json() == searchResultBody

    deleteAfterTest(uid1)
    deleteAfterTest(uid2)
    deleteAfterTest(uid3)
    
    response = client.get("/search/test+success")
    assert response.status_code == 200
    assert response.json() == {}
    deleteAfterTest(uid4)

def test_getAll():
    response = client.get("/all")
    assert response.status_code == 200

def test_NotAnEndpoint():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}