from eve import Eve
import psutil
import platform
from datetime import datetime
from flask import jsonify


app = Eve()

#Converts input into json then response object
def response(resourcedata):
    #The first two lines could have also been written with the json and flask.Response library as shown directly below:
    #jsondata = json.dumps(resourcedata)
    #response=Response(response=jsondata, status=200, content_type="application/json;charset=utf-8")
    response = jsonify(resourcedata)
    response.status_code=200
    return response


#RAM data
@app.route('/resource/ram', methods=['GET'])
def ram():
    ramdata = {
            "Total (bytes)": psutil.virtual_memory().total,
            "Available (bytes)": psutil.virtual_memory().available,
            "Percent": psutil.virtual_memory().percent,
            "Used (bytes)": psutil.virtual_memory().used,
            "Free (bytes)": psutil.virtual_memory().free
            }
    return (response(ramdata))

#General system data of underlying platform (including processor)
@app.route("/resource/platform", methods=["GET"])
def uname():
    unamedata = {
            "Node": platform.uname().node,
            "System": platform.uname().system,
            "Release": platform.uname().release,
            "Version": platform.uname().version,
            "Machine": platform.uname().machine,
            "Processor": platform.uname().processor #Note: may return processor id or same value as Machine depending on instance.
            }
    return(response(unamedata))


#Disk Usage data
@app.route("/resource/diskspace", methods=["GET"])
def disk():
    diskdata = {
            "Total (bytes)": psutil.disk_usage('/').total,
            "Used (bytes)": psutil.disk_usage('/').used,
            "Free (bytes)": psutil.disk_usage('/').free,
            "Percent": psutil.disk_usage('/').percent,
            }
    return(response(diskdata))

#User data
@app.route("/resource/user", methods=["GET"])
def user():
    userdata = {
            "User": psutil.users()[0].name,
            "Terminal": psutil.users()[0].terminal,
            "Host": psutil.users()[0].host,
            "StartTime": datetime.fromtimestamp(psutil.users()[0].started).strftime("%m-%d-%Y %H:%M:%S")

            }
    return(response(userdata))



if __name__=='__main__':
    app.run()
    
    
#http://127.0.0.1:5000/resource/ram
#http://127.0.0.1:5000/resource/platform
#http://127.0.0.1:5000/resource/diskspace
#http://127.0.0.1:5000/resource/user