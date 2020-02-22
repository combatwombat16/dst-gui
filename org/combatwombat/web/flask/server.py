from flask import Flask, request, jsonify, Blueprint
from org.combatwombat.dst.config.Server import Server, ServerSchema
from org.combatwombat.dst.config.Cluster import Cluster, ClusterSchema
from org.combatwombat.web.flask import settings
from configparser import ConfigParser
from os import path

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    flask_app.register_blueprint(blueprint)


@app.route('/')
def index():
    """Base page"""
    return "Don't Starve Together Server Management ReST API Backend"


@app.route('/api/v1')
def info():
    """API Information Page"""
    output = {
        "index": "GET /",
        "info": "GET /api/v1",
        "Write default cluster.ini": "GET /config/cluster/write",
        "Write configured cluster.ini": "POST /config/cluster/write",
        "Create cluster config": "GET /config/cluster/read",
        "Read cluster config": "POST /config/cluster/read",
        "Write default server.ini": "GET /config/server/write",
        "Write configured server.ini": "POST /config/server/write",
        "Create server config": "GET /config/server/read",
        "Read server config": "POST /config/server/read"
    }

    return jsonify(output)


@app.route('/config/cluster/write', methods=['GET', 'POST'])
def cluster_write():
    """Write cluster configuration to cluster.ini"""
    if request.method == "POST":
        content = request.json
        if 'config' in content:
            cluster = ClusterSchema().loads(content['config'])
        else:
            cluster = Cluster()

        if 'path' in content:
            cluster.write_ini(content['path'])
        else:
            cluster.write_ini('./cluster.ini')
    else:
        cluster = Cluster()
        cluster.write_ini('./cluster.ini')

    return "wrote configuration as follows:\n {}".format(cluster.to_json())


@app.route('/config/cluster/read', methods=['GET', 'POST'])
def cluster_read():
    """Read cluster configuration from cluster.ini or make default configuration"""
    cluster_schema = ClusterSchema()
    if request.method == "POST":
        content = request.json
        if 'config' in content:
            cluster = cluster_schema.load(content['config'])
        elif 'path' in content:
            config_data = ConfigParser()
            if path.exists(content['path']):
                with open(content['path'], 'r') as in_file:
                    config_data.read(in_file)
                    cluster = cluster_schema.load(config_data._sections)
            else:
                return 'Specified file not found.'
        else:
            return 'No valid options specified in post'
    else:
        cluster = Cluster()

    return cluster.to_json()


@app.route('/config/server/write', methods=['GET', 'POST'])
def server_write():
    """Write server configuration to server.ini"""
    if request.method == "POST":
        content = request.json
        if 'config' in content:
            server = ServerSchema().load(content['config'])
        else:
            server = Server()

        if 'path' in content:
            server.write_ini(content['path'])
        else:
            server.write_ini('./server.ini')
    else:
        server = Server()
        server.write_ini('./server.ini')

    return "wrote configuration as follows:\n {}".format(server.to_json())


@app.route('/config/server/read', methods=['GET', 'POST'])
def server_read():
    """Read server configuration from server.ini or make default configuration"""
    server_schema = ServerSchema()
    if request.method == "POST":
        content = request.json
        if 'config' in content:
            server = server_schema.load(content['config'])
        elif 'path' in content:
            config_data = ConfigParser()
            if path.exists(content['path']):
                with open(content['path'], 'r') as in_file:
                    config_data.read(in_file)
                    server = server_schema.load(config_data._sections)
            else:
                return 'Specified file not found.'
        else:
            return 'No valid options specified in post'
    else:
        server = Server()

    return server.to_json()


def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()


