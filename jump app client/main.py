import tarfile
import feather
import json
from os.path import isfile
from os import remove
import pandas as pd
from sys import platform
from requests import get
from os.path import basename
from time import sleep
server_ip = "http://127.0.0.1:5001"


def check_settings():
    if isfile("./data/settings.feather") == False:
        print("Settings File not found\nDefault Config File will created")
        settings = pd.DataFrame({
            "OS": platform
        }, index=[1]).reset_index()
        settings.to_feather("./data/settings.feather")

#make Settings Feather to json
settings_df = pd.read_feather("./data/settings.feather").to_json()
settings_json = json.loads(settings_df)

#Get OS
OS = settings_json["OS"]
OS = OS["0"]
def getlink(appname,name):
    for key in appname.keys():
        current = appname[str(key)]
        app_os = loaded_rasp["OS"];app_os = app_os[key]
        if str(current) == name and OS == app_os:
            print(key)
            print(app_os)
            return applink[str(key)] , key

check_settings()

#Update Package-list
rasp = get(f"{server_ip}/db/json").content.decode()
pd.read_json(rasp).to_feather("./data/rasp.feather")

#get name from Package in next this work with args

name = input("App Name: ")

#some more Variables
loaded_rasp = json.loads(rasp)
appname = loaded_rasp["appname"]
applink = loaded_rasp["applink"]
link , id = getlink(appname,name)
app_os = loaded_rasp["OS"]
app_os = app_os[id]
filename = basename(link)
x = get(link).content
#Download and unpack Package
