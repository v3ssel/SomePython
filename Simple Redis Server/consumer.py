#!/usr/bin/python3
import sys
import redis
import json
import logging

logging.basicConfig(level=logging.INFO)

def create_bad_guys():
    bad_guys = []
    if len(sys.argv) == 3 and sys.argv[1] == '-e':
        bad_guys = [int(a) for a in sys.argv[2].split(',') if len(a) == 10]
    elif len(sys.argv) == 2 and len(sys.argv[1]) == 10:
        bad_guys.append(int(sys.argv[1]))
    return bad_guys

def main_process():
    bad_guys = create_bad_guys()

    client = redis.Redis(host='localhost', port=6379)
    channel = client.pubsub(ignore_subscribe_messages=True)
    channel.subscribe('redis_channel')

    for message in channel.listen():
        m = json.loads(message['data'])
        if int(m['metadata']['to']) in bad_guys and int(m['amount']) >= 0:
            m['metadata']['to'], m['metadata']['from'] = m['metadata']['from'], m['metadata']['to']
        logging.info(m)

if __name__ == '__main__':
    main_process()
