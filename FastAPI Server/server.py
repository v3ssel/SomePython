import json
import urllib.parse
import uuid
import fastapi
import uvicorn
import httpx
from pydantic import BaseModel
from typing import List


app = fastapi.FastAPI()


class Url(BaseModel):
    url: List[str]


class UrlList(BaseModel):
    data: List[Url]


class Item(BaseModel):
    url: Url
    ID: uuid.UUID
    status: str


@app.get('/')
async def hello():
    return {"Hello": "World"}


@app.post('/api/v1/tasks/', status_code=201)
async def receive_data(data: UrlList):
    tmp = data.dict()
    return Item(url={'url': data.data[0].url}, ID=uuid.uuid4(), status='running')


@app.get('/api/v1/tasks/{data}', status_code=201)
async def show_data(data: str):
    query = urllib.parse.parse_qs(data)
    url_list = query['url'][0]
    jas = url_list.replace("'", "\"")
    url_list = json.loads(jas)
    url = ""
    for i in url_list['url']:
        url += i + '/'
    url = url[:-1]
    query.update({'url': [url]})
    items = {}
    async with httpx.AsyncClient() as client:
        get = await client.get('https://' + url)
        items.update({str(get.status_code): url})
    return items


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8888)
