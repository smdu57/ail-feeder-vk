import argparse
import configparser
import json

import vk

config = configparser.ConfigParser()
config.read('./Vk-feed.cfg')

if not config.sections():
    print("Please be sure to have config file correctly named 'Vk-feed.cfg' in root directory")
    input("Press any key to exit")
    exit()
else:
    if 'general' in config and 'vk_api':
        token = config['general']['token']
        default_limit = config['general']['default_limit']
        version = config['vk_api']['version']
        language = config['vk_api']['language']
    else:
        print("There is an error reading the file, be sure it look the same as the example")
        input("Press any key to exit")
        exit()
session = vk.Session(access_token=token)
api = vk.API(session, v=version, lang=language)
argument = argparse.ArgumentParser(description='String research on VK')
argument.add_argument('query', metavar='String', type=str, help='Term you want to search on VK')
argument.add_argument('--limit', metavar='N', type=int, default=default_limit, help='Request limit (default is '+default_limit)
arguments = argument.parse_args()

result = api.search.getHints(q=arguments.query, limit=arguments.limit)
jsonString = json.dumps(result)
print(result)
