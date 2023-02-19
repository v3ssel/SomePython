import asyncio
import urllib.parse
import httpx
import json
import sys


async def to_server(url):
    if url[:7] == 'http://': url = url[7:]
    if url[:8] == 'https://': url = url[8:]
    api_url = "http://localhost:8888/api/v1/tasks/"
    urls = {'data': [{"url": str(url).split('/')} for i in sys.argv[1:]]}
    async with httpx.AsyncClient() as client:
        resp = await client.post(api_url, data=json.dumps(urls))

    task = resp.content.decode('utf-8')
    json_acceptable_string = task.replace("'", "\"")
    task = json.loads(json_acceptable_string)
    task_url = api_url + urllib.parse.urlencode(task)
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(task_url)
            resp.raise_for_status()
        res = resp.json()
        for i in res.keys():
            print(f'{i}\thttps://{res[i]}')
    except:
        pass


if __name__ == '__main__':
    tasks = list()
    for link in sys.argv[1:]:
        tasks.append(asyncio.ensure_future(to_server(link)))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
