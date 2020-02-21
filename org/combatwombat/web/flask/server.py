from flask import Flask, request
from org.combatwombat.dst.config.Server import Server, ServerSchema
from org.combatwombat.dst.config.Cluster import Cluster, ClusterSchema
import json

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def hello_world():
    return "Don't Starve Together Web GUI"


@app.route('/config/cluster/show', methods=['GET'])
def cluster_show():
    clus = Cluster()
    return clus.to_json()


@app.route('/config/cluster/write', methods=['GET'])
def cluster_write():
    clus = Cluster()
    clus.write_ini('./cluster.ini')
    return "wrote configuration as follows:\n {}".format(clus.to_json())


@app.route('/config/cluster/read', methods=['POST'])
def cluster_read():
    content = request.json
    cluster_schema = ClusterSchema()
    cluster = cluster_schema.load(content['config'])
    return cluster.to_json()


@app.route('/config/server/show', methods=['GET'])
def server_show():
    srv = Server()
    return srv.to_json()


@app.route('/config/server/write', methods=['GET'])
def server_write():
    srv = Server()
    srv.write_ini('./server.ini')
    return "wrote configuration as follows:\n {}".format(srv.to_json())


@app.route('/config/server/read', methods=['POST'])
def server_read():
    content = request.json
    server_schema = ServerSchema()
    server = server_schema.load(content['config'])
    return server.to_json()
