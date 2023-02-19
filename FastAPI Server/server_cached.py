import json
import aioredis
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
    redis = aioredis.Redis.from_url(
        "redis://localhost", max_connections=10, decode_responses=True
    )
    query = urllib.parse.parse_qs(data)
    url_list = query['url'][0]
    jas = url_list.replace("'", "\"")
    url_list = json.loads(jas)
    url = ""
    for i in url_list['url']:
        url += i + '/'
    url = url[:-1]
    domain = url_list['url'][0] + '/'
    query.update({'url': [url]})
    items = {}

    domain_cache = await redis.get(domain)
    if domain_cache is not None:
        domain_cache = json.loads(domain_cache.replace("'", "\"")[1:-1])
        domain_cache.update({'count': [str(int(domain_cache['count'][0]) + 1)]})
        await redis.set(domain, json.dumps(str(domain_cache)), ex=100)
    else:
        count = {'count': ['1']}
        await redis.set(domain, json.dumps(str(count)), ex=100)
    print(domain_cache)

    cache = await redis.get(url)
    if cache is not None:
        cache = json.loads(cache.replace("'", "\"")[1:-1])
        items.update({cache['status_code'][0]: cache['url'][0]})
        print(cache)
        await redis.set(url, json.dumps(str(cache)), ex=100)
        return items

    async with httpx.AsyncClient() as client:
        get = await client.get('https://' + url)
        query.update({'status_code': [str(get.status_code)], 'status': ['ready']})
        items.update({str(get.status_code): url})
    await redis.set(url, json.dumps(str(query)), ex=100)
    return items


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8888)
