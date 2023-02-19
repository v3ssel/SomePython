#!/usr/bin/python3
import redis
import json
import logging

r = redis.StrictRedis(host='localhost', port=6379, charset="utf-8", decode_responses=True)
client = redis.Redis(host='localhost', port=6379)
channel = client.pubsub()
channel.subscribe('redis_channel')

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    messages = [{"metadata": {"from": 1111111111, "to": 2222222222}, "amount": 10000},
                {"metadata": {"from": 3333333333, "to": 4444444444}, "amount": -3000},
                {"metadata": {"from": 2222222222, "to": 5555555555}, "amount": 5000}]
    
    for message in messages:
        client.publish('redis_channel', json.dumps(message))
        logging.info(message)
