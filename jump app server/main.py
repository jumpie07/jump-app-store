import flask
from flask import send_from_directory
import feather
import pandas as pd
from os.path import isfile
import tarfile

app = flask.Flask(__name__)
rasp_path = "./data/rasp.feather"
if not isfile(rasp_path):
    print("test")
    pd.DataFrame({}).reset_index().to_feather(rasp_path)
rasp = pd.read_feather(rasp_path)
def addapp(applink,appname,cat,filepath):
    column = rasp["index"]
    max_value = column.max()
    max_index = max_value
    df = pd.DataFrame({
        "appname" : appname,
        "applink" : applink,
        "cat" : cat
    },index=[max_index + 1,max_index + 2,max_index + 3])
    frames = [df]
    results = pd.concat(frames).reset_index()
    results.to_feather(rasp_path)

addapp("http://127.0.0.1:5001/apps/test.tar.gz","test","test","test")


@app.route("/db")
def test():
    text = pd.read_feather(rasp_path).to_html()
    return text

@app.route("/db/json")
def return_feather():
    return pd.read_feather(rasp_path).to_json()

@app.route("/apps/<name>")
def return_file(name):
    try:
        return send_from_directory("./apps", filename=name, as_attachment=True)
    except:
        return "404"
if __name__ == "__main__":
    app.run(port=5001,debug=True)