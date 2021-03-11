import os
import redis
import csv
from google.cloud import storage

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)
storage_client = storage.Client()
increment = 1

def attempt_count():
    """Increments the attempt Redis counter and prints the current value."""
    value = redis_client.incr('attempt', increment)
    print('Current attempt count: {}'.format(value))
    
def success_count():
    """Increments the success Redis counter and prints the current value."""
    value = redis_client.incr('success', increment)
    print('Current success count: {}'.format(value))
    
def gcsdownloader(event, context):
    """Entrypoint, downloads GCS blob and inserts IP addresses into Redis."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(event['bucket'])
    blob = bucket.blob(event['name'])
    csvstring = blob.download_as_bytes().decode("utf-8")
    lines = csvstring.splitlines()

    attempt_count()

    for row in csv.reader(lines,delimiter=","):
        redis_client.zincrby("ipaddr", increment, row[3])
        
    success_count()
    redis_client.connection_pool.disconnect()