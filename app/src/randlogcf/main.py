import os
import random
import math
import time
import uuid
from google.cloud import storage


map = [[],[],[],[]]


def ipaddr():
    """Generates a random IP address."""
    def remap(num, offset):
        """Shuffles the map list and returns (str) a number between 0 and 254."""
        num = num % 255
        if not map[offset]:
            map[offset] = list(range(255))
            random.shuffle(map[offset])
        return(str(map[offset][num]))


    def octet(offset):
        """Returns a random octect value (str) for a given offset.
        
        Uses math.gcd to create a set of IP addresses biased towards a few IPs instead of random noise.
        """
        max = 65025
        return remap(round(math.gcd(random.randint(1,max), random.randint(0,max))), offset)

    ip = '.'.join([octet(0), octet(1), octet(2), octet(3)])
    return ip

def randrequest():
    """Generates random request type from list."""
    request_list = ["GET", "POST"]
    return random.choice(request_list)

def randpath():
    """Generates random path from list."""
    path_list = ["/index.html", "/exchange.php", "/metrics.app", "/about.html", "/contact.html", "/banner.png", "/menu.html", "/logo.png"]
    return random.choice(path_list)

def gcsuploader(destination_bucket_name, destination_blob_name, input_string):
    """Uploads blob to GCS, returns bucket and blob names."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(destination_bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(input_string)
    return destination_blob_name, destination_bucket_name

def randlogcf(request):
    """Entrypoint, generates and uploads blob to GCS."""
    loglines = ""
    bucket_env_var = os.environ.get('DESTINATION_BUCKET', "DESTINATION_BUCKET environment variable not set.")
    current_epoch_time = int(time.time())
    anchor_epoch_time = current_epoch_time - 3000000
    unique_blob_name = str(uuid.uuid4()) + "_" + str(current_epoch_time)

    for x in range(255000):
        rand_epoch_time = random.randrange(anchor_epoch_time, current_epoch_time, 1)
        logline = str(rand_epoch_time) + "," + randrequest() + "," + randpath() + "," + ipaddr() + "\n"
        loglines += logline
    
    message_blob_name, message_bucket_name = gcsuploader(
        destination_bucket_name=bucket_env_var, destination_blob_name=unique_blob_name, input_string=loglines
    )

    print(
        "Created a new object {} in the bucket {}".format(
            message_blob_name, message_bucket_name
        )
    )