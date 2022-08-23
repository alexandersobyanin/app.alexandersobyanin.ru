#!python3
import os
import json
from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask_sslify import SSLify
from flask_cors import cross_origin

from environment_variables import environment_variables
from environment_variables import SEO
from wheellog_csv.wheellog_csv import wheellog_csv
from tracker_announce.tracker_announce import tracker_announce

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(wheellog_csv, url_prefix='/wheellog_csv')
app.register_blueprint(tracker_announce, url_prefix='/tracker_announce')
app.debug = False
sslify = SSLify(app)

global_context = {}
global_context.update(environment_variables)


@app.route('/', methods=['GET'])
def root():
    return render_template('root.html', **global_context)


@app.route('/health.php', methods=['GET'])
@cross_origin(origins=['https://alexandersobyanin.ru'], methods=['GET'])
def health():
    return '{"health":1}'


@app.route('/ads.txt', methods=['GET'])
def ads():
    return 'google.com, pub-{id}, DIRECT, f08c47fec0942fa0'.format(id=SEO.google.adsense_id)


@app.route('/.well-known/acme-challenge/<certbot_key>', methods=['GET'])
def certbot(certbot_key):
    certbot_pass = json.loads(os.environ['CERTBOT_KEYS']).get(certbot_key)
    if not certbot_pass:
        return 'FAILED'
    return '{}.{}'.format(certbot_key, certbot_pass)


@app.route('/csv_to_gpx', methods=['GET'])
def csv_to_gpx():
    return redirect(url_for('wheellog_csv.wheellog_csv_form'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
