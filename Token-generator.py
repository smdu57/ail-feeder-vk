import configparser
import json
from urllib.request import urlopen
import getpass

print("To generate a VK token, you need a VK account")
print("You can directly go to this link : https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=YOUT_ACCOUNTS_LOGIN&password=YOUR_ACCOUNT_PASSWORD")
print("and replace YOUR_ACCOUNTS_LOGIN and YOUR_ACCOUNT_PASSWORD by your account credentials")
print("or you can generate your token using this program by typing 1")
x = input()
if x == '1':
    while 1:
        user = input("Pls enter your login : ")
        password = getpass.getpass('Pls enter your password : ')
        url = "https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username="+user+"&password="+password
        try:
            response = urlopen(url)
        except Exception:
            print("Invalid credentials")
            continue
        break
    data = json.loads(response.read())
    token = data['access_token']
    print("your token : "+token)
    while 1:
        a = input("Would you like to update config file with token directly ? y/n ")
        if a == 'y':
            config = configparser.ConfigParser()
            config.read('./Vk-feed.cfg')
            if 'vk_api' in config:
                config.set('vk_api', 'token', token)
            else:
                config.add_section('vk_api')
                config.set('vk_api', 'token', token)
            file = open('Vk-feed.cfg', 'w')
            config.write(file)
            print("Config file modified successfully")
            break
        if a == 'n':
            input("You must copy your token in api parameter in the config file")
            break
    exit()
else:
    exit()
