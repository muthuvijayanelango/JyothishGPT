import google
import google.auth
from google.cloud import storage
import json
import sys

credentials, project = google.auth.default()  
#List buckets using the default account on the current gcloud cli
client = storage.Client(credentials=credentials)
buckets = client.list_buckets()
for bucket in buckets:
    print(bucket)

#custom function to read data in json file
def get_json_gcs(bucket_name, file_name):
    # create storage client
    client = storage.Client()
    # get bucket with name
    BUCKET = client.get_bucket(bucket_name)

    # get the blob
    blob = BUCKET.get_blob(file_name)

    # load blob using json
    file_data = json.loads(blob.download_as_string())
    return file_data

def RetrieveCache(usrquery):
    try:
        print(sys.path)
        bucket_name = "jyothish_bucket1"
        file_name = "cache.json"
        json_data = get_json_gcs(bucket_name, file_name)
        cacheresponse = str(json_data[usrquery])
        return cacheresponse
    except KeyError:
        print("Key Error")
        return ""