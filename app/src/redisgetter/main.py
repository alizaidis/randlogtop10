import os
import json
import redis

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

def redisgetter():
    """Gets current top 10 IPs and counts from Redis and returns a dict."""
    redis_list = redis_client.zrevrange("ipaddr", 0, 9, withscores = True)
    json_dict = {}

    for tuple in redis_list:
	    element_one = tuple[0].decode("utf-8")
	    element_two = int(tuple[1])
	    json_dict[element_one] = element_two
    
    return json_dict

def jsonresponse(request):
    """Entrypoint, returns top 10 IPs and counts as JSON."""
    data = redisgetter()
    return json.dumps(data), 200, {'ContentType': 'application/json'}