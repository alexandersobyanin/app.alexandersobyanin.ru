#!python3
import codecs
import csv
import datetime
import os
import json
import socket
import urllib.error
import urllib.parse
import urllib.request
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask_sslify import SSLify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from seo import SEO

app = Flask(__name__, static_url_path='/static')
app.debug = False
sslify = SSLify(app)

global_context = {'SEO': SEO}


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


@app.route('/tracker_announce/<path:tracker_path>', methods=['GET'])
def tracker_announce(tracker_path):
    pass_key = request.args.get('pk')
    if pass_key != os.environ.get('tracker_pass_key'):
        return Response(response='Unauthorized', status=401)
    params = urllib.parse.urlencode(request.args)
    url = f'http://{tracker_path}?{params}'
    return Response(response=f'url={url}', status=200)
    try:
        with urllib.request.urlopen(url, timeout=1) as response:
            response_code = response.status
            response_content = response.read()
            response_content_type = response.getheader('Content-Type')
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout) as e:
        response_code = 200
        response_content = f'We failed to reach a tracker: {e}'
        response_content_type = 'text/html; charset=UTF-8;'
    return Response(response=response_content, content_type=response_content_type, status=response_code)


@app.route('/csv_to_gpx/', methods=['GET'])
def csv_to_gpx_form():
    return render_template('csv_to_gpx/form.html', **global_context)


@app.route('/csv_to_gpx/', methods=['POST'])
def csv_to_gpx_process():
    def generate_gpx():
        for row in gpx_rows:
            yield f"{row}\n"
    if 'csvSelect' not in request.files:
        return Response(response='No file part', status=400)
    file = request.files['csvSelect']
    if file.filename == '':
        return Response(response='No selected file', status=400)
    if file and file.filename.rsplit('.', 1)[1].lower() != 'csv':
        return Response(response='No allowed file', status=400)
    start_time = None
    min_lat = None
    min_lon = None
    max_lat = None
    max_lon = None
    max_speed = None
    max_gps_speed = None
    max_pwm = None
    file.seek(0)
    csv_reader = csv.DictReader(codecs.iterdecode(file, 'utf-8'))
    for row in csv_reader:
        if start_time is None:
            start_time = datetime.datetime.strptime(f"{row['date']} {row['time']}", '%Y-%m-%d %H:%M:%S.%f')
        if min_lat is None:
            min_lat = row['latitude']
        if row['latitude'] < min_lat:
            min_lat = row['latitude']
        if max_lat is None:
            max_lat = row['latitude']
        if row['latitude'] > max_lat:
            max_lat = row['latitude']
        if min_lon is None:
            min_lon = row['longitude']
        if row['longitude'] < min_lon:
            min_lon = row['longitude']
        if max_lon is None:
            max_lon = row['longitude']
        if row['longitude'] > max_lon:
            max_lon = row['longitude']
        if max_speed is None:
            max_speed = row['speed']
        if row['speed'] > max_speed:
            max_speed = row['speed']
        if max_gps_speed is None:
            max_gps_speed = row['gps_speed']
        if row['gps_speed'] > max_gps_speed:
            max_gps_speed = row['gps_speed']
        if max_pwm is None:
            max_pwm = row['pwm']
        if row['pwm'] > max_gps_speed:
            max_pwm = row['pwm']
    gpx_rows = [
        '<?xml version="1.0"?>',
        '<gpx version="1.1"',
        ' creator="CSV to GPX - https://app.alexandersobyanin.ru/csv_to_gpx/"',
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        ' xmlns="http://www.topografix.com/GPX/1/1"',
        ' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">',
        ' <metadata>',
        f'  <time>{start_time.isoformat()}</time>',
        f'  <bounds minlat="{min_lat}" minlon="{min_lon}" maxlat="{max_lat}" maxlon="{max_lon}"/>',
        ' </metadata>',
        ' <trk>',
        f'  <name>{file.filename.replace(".csv", "")}</name>',
        '  <trkseg>',
    ]
    gpx_rows.extend([
        '  </trkseg>',
        ' </trk>',
        '</gpx>'
    ])
    return app.response_class(
        generate_gpx(),
        mimetype='application/gpx+xml',
        headers={'Content-Disposition': f'attachment; filename={file.filename.replace(".csv", ".gpx")}'}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
