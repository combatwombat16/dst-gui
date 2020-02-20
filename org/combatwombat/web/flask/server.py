from flask import Flask
from org.combatwombat.dst.config.Server import Server
from json import dumps
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/config/server', methods=['GET'])
def server():
    srv = Server()
    return dumps(Server)
