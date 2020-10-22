# Application to squirro README

Here is the documentation on how to run the code:


## Installation

#### ElasticSearch Host Download Link

[Windows](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.2-windows-x86_64.zip)

[Mac](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.2-darwin-x86_64.tar.gz)

Move to the folder `.\elasticsearch-7.9.2` and run on the terminal: `bin/elasticsearch`

Test if elasticsearch is running: `curl http://localhost:9200/`


#### Install python requirements

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
This should install 4 library: `elasticsearch`, `fastapi`, `pytest`, `uvicorn`


## Usage

Run the server with: 
```bash
uvicorn main:app --reload
```

You can find the swagger following : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

or

Import Postman Collection 

## Run Tests

```bash
pytest main-test.py
```
