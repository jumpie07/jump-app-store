import tarfile

import feather
import json
from os.path import isfile
from os import remove
import pandas as pd
from sys import platform
from requests import get

server_ip = "http://127.0.0.1:5000"


def check_settings():
    if isfile("./data/settings.feather") == False:
        print("Settings File not found\nDefault Config File will created")
        settings = pd.DataFrame({
            "OS": platform
        }, index=[1]).reset_index()
        settings.to_feather("./data/settings.feather")

def getlink(appname,name):
    for key in appname.keys():
        current = appname[str(key)]
        if str(current) == name:
            return applink[str(key)]
check_settings()

settings_df = pd.read_feather("./data/settings.feather").to_json()
settings_json = json.loads(settings_df)
OS = settings_json["OS"]
OS = OS["0"]
rasp = get(f"{server_ip}/db/json").content.decode()
pd.read_json(rasp).to_feather("./data/rasp.feather")
name = input("App Name: ")
loaded_rasp = json.loads(rasp)
appname = loaded_rasp["appname"]
applink = loaded_rasp["applink"]

link = getlink(appname,name)

open(f"./temp/{appname}.tar.gz","w").write(get(link).content)
downloaded = tarfile.open(f"./temp/{appname}.tar.gz","r:gz")
downloaded.extractall()
downloaded.close()
remove(f"./temp/{appname}.tar.gz")
