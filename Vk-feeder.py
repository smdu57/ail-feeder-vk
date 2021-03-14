import argparse
import base64
import configparser
import gzip
import hashlib
import json
import redis
import requests
import vk
from vk.exceptions import VkAPIError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
config = configparser.ConfigParser()
config.read('./Vk-feed.cfg')

if not config.sections():
    print("Please be sure to have config file correctly named 'Vk-feed.cfg' in root directory")
    input("Press any key to exit")
    exit()
else:
    if 'general' in config and 'vk_api' and 'redis' and 'ail':
        default_limit = config['general']['default_limit']
        token = config['vk_api']['token']
        version = config['vk_api']['version']
        language = config['vk_api']['language']
        host = config['redis']['host']
        port = config['redis']['port']
        ail = config['ail']['url']
        apik = config['ail']['api']
    else:
        print("There is an error reading the file, be sure it look the same as the example")
        input("Press any key to exit")
        exit()
try:
    r = redis.Redis(host=host, port=port, db=0)
except Exception:
    input("Error connecting to redis db")
    exit()
session = vk.Session(access_token=token)
api = vk.API(session, v=version, lang=language)
argument = argparse.ArgumentParser(description='String research on VK')
argument.add_argument('query', metavar='String', type=str, help='Term you want to search on VK')
argument.add_argument('--limit', metavar='N', type=int, default=default_limit, help='Request limit (default is ' + default_limit)
arguments = argument.parse_args()

try:
    profiles = api.search.getHints(q=arguments.query, limit=arguments.limit)
    docs = api.docs.search(q=arguments.query, count=arguments.limit)["items"]
    news = api.newsfeed.search(q=arguments.query, count=arguments.limit)["items"]
    photos = api.photos.search(q=arguments.query, count=arguments.limit)["items"]
except VkAPIError as e:
    input(e.message)
    exit()
jsonString = json.dumps(profiles)

for obj in profiles:
    data = {'source': 'VK feeder', 'source-uuid': 'bdf86b8c-edcf-40b8-9f39-a34242df6181', 'default-encoding': 'UTF-8','meta': {}}
    if obj['type'] == 'group':
        if r.exists("c:{}".format(obj['group']['id'])):
            print("Data already in DB")
            continue
        r.set("c:{}".format(obj['group']['id']), obj['description'])
        data['meta']['vk:id'] = obj['group']['id']
        data['meta']['vk:name'] = obj['group']['name']
        data['meta']['vk:screen_name'] = obj['group']['screen_name']
        data['meta']['vk:photo'] = obj['group']['photo_50']
    else:
        if r.exists("c:{}".format(obj['profile']['id'])):
            print("Data already in DB")
            continue
        r.set("c:{}".format(obj['profile']['id']), obj['description'])
        data['meta']['vk:id'] = obj['profile']['id']
        data['meta']['vk:name'] = obj['profile']['first_name']+" "+obj['profile']['last_name']
    data['data'] = str(base64.b64encode(gzip.compress(obj['description'].encode())))
    m = hashlib.sha256()
    m.update(obj['description'].encode('utf-8'))
    data['data-sha256'] = m.hexdigest()
    response = requests.post(ail, headers={'Content-Type': 'application/json', 'Authorization': apik}, data=json.dumps(data), verify=False)
    print(response)
