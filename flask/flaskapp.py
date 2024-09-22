from flask import Flask, request
import json
import ja

app = Flask(__name__)

@app.route('/') 
def hello_world():
    vars = ["SSL_SESSION_ID", "SSL_CLIENTHELLO_VERSION", "SSL_CLIENTHELLO_CIPHERS", "SSL_CLIENTHELLO_EXTENSIONS", "SSL_CLIENTHELLO_GROUPS", "SSL_CLIENTHELLO_EC_FORMATS", "SSL_CLIENTHELLO_SIG_ALGOS", "SSL_CLIENTHELLO_ALPN", "SSL_CLIENTHELLO_VERSIONS"]
    data = {}
    for v in vars:
        data[v] = request.environ.get(v)
    data['ja3'] = ja.ja3(data)
    data['ja4'] = ja.ja4(data)
    data['optimal'] = ja.optimal(data)
    return json.dumps(data)

if __name__ == '__main__':
   app.run()
