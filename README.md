# Ail-feeder-vk

This script provide data from VK.com to feed the application AIL Project via a string query.

##Install

~~~shell
pip install -r requirements.txt
~~~
OR
~~~shell
pip3 install -r requirements.txt
~~~

##Usage

~~~shell

usage: Vk-feeder.py [-h] [--limit N] String

String research on VK

positional arguments:
  String      Term you want to search on VK

optional arguments:
  -h, --help  show this help message and exit
  --limit N   Request limit (default is 50)

~~~

##Json output
~~~~Shell
Vk-feeder.py --limit 2 Irina
~~~~
~~~json
[
   {
      "type": "profile",
      "profile": {
         "first_name": "Irina",
         "id": 10059,
         "last_name": "Pankratova",
         "can_invite_to_chats": false
      },
      "section": "people",
      "description": "34 years old, vk.com/irina"
   },
   {
      "type": "profile",
      "profile": {
         "first_name": "Irina",
         "id": 140223263,
         "last_name": "Vaymer",
         "can_invite_to_chats": false
      },
      "section": "people",
      "description": "21 years old, vk.com/irinawaimer"
   }
]
~~~