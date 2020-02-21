from flask import Flask
from org.combatwombat.dst.config.Server import Server
from org.combatwombat.dst.config.Cluster import Cluster


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/config/server/show', methods=['GET'])
def server():
    srv = Server()
    return srv.to_json()


@app.route('/config/cluster/write', methods=['GET'])
def cluster_write():
    clus = Cluster()
    clus.write_ini('./cluster.ini')
    return "wrote configuration as follows:\n {}".format(clus.to_json())


@app.route('/config/cluster/show', methods=['GET'])
def cluster():
    clus = Cluster()
    return clus.to_json()


@app.route('/config/server/write', methods=['GET'])
def server_write():
    srv = Server()
    srv.write_ini('./server.ini')
    return "wrote configuration as follows:\n {}".format(srv.to_json())
