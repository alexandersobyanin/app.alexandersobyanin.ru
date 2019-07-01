#!python3
import os
import json
from flask import Flask
from flask import render_template
from flask_cors import cross_origin

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def root():
    return render_template('root.html')


@app.route('/health.php', methods=['GET'])
@cross_origin(origins=['https://alexandersobyanin.ru'], methods=['GET'])
def health():
    return '{"health":1}'


@app.route('/ads.txt', methods=['GET'])
def ads():
    return 'google.com, pub-{id}, DIRECT, f08c47fec0942fa0'.format(id=os.environ['GOOGLE_ADSENSE_ID'])


@app.route('/.well-known/acme-challenge/<certbot_key>', methods=['GET'])
def certbot(certbot_key):
    certbot_pass = json.loads(os.environ['CERTBOT_KEYS']).get(certbot_key)
    if not certbot_pass:
        return 'FAILED'
    return '{}.{}'.format(certbot_key, certbot_pass)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
