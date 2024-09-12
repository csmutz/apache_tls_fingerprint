from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/') 
def hello_world():
    vars = ["SSL_SESSION_ID", "SSL_CLIENTHELLO_VERSION", "SSL_CLIENTHELLO_CIPHERS", "SSL_CLIENTHELLO_EXTENSION_IDS", "SSL_CLIENTHELLO_EC_GROUPS", "SSL_CLIENTHELLO_EC_FORMATS", "SSL_CLIENTHELLO_SIG_ALGOS", "SSL_CLIENTHELLO_ALPN", "SSL_CLIENTHELLO_COMP_METHODS","SSL_CLIENTHELLO_SUPPORTED_VERSIONS"]
    data = {}
    for v in vars:
        data[v] = request.environ.get(v)
    return json.dumps(data)

if __name__ == '__main__':
   app.run()
