#!python3
import codecs
import csv
import datetime
from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template

from environment_variables import environment_variables

csv_to_gpx = Blueprint('csv_to_gpx', __name__, template_folder='templates')

global_context = {}
global_context.update(environment_variables)


@csv_to_gpx.route('/', methods=['GET'])
def csv_to_gpx_form():
    return render_template('form.html', **global_context)


@csv_to_gpx.route('/', methods=['POST'])
def csv_to_gpx_process():
    def generate_gpx():
        for _row in gpx_rows:
            yield f"{_row}\n"
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
    max_temperature = None
    file.seek(0)
    csv_reader = csv.DictReader(codecs.iterdecode(file, 'utf-8'))
    for row in csv_reader:
        latitude = float(row['latitude'])
        longitude = float(row['longitude'])
        gps_speed = float(row['gps_speed'])
        speed = float(row['speed'])
        pwm = float(row['pwm'])
        temperature = float(row['system_temp'])
        if start_time is None:
            start_time = datetime.datetime.strptime(f"{row['date']} {row['time']}", '%Y-%m-%d %H:%M:%S.%f')
        if min_lat is None:
            min_lat = latitude
        if latitude < min_lat:
            min_lat = latitude
        if max_lat is None:
            max_lat = latitude
        if latitude > max_lat:
            max_lat = latitude
        if min_lon is None:
            min_lon = longitude
        if longitude < min_lon:
            min_lon = longitude
        if max_lon is None:
            max_lon = longitude
        if longitude > max_lon:
            max_lon = longitude
        if max_speed is None:
            max_speed = speed
        if speed > max_speed:
            max_speed = speed
        if max_gps_speed is None:
            max_gps_speed = gps_speed
        if gps_speed > max_gps_speed:
            max_gps_speed = gps_speed
        if max_pwm is None:
            max_pwm = pwm
        if pwm > max_gps_speed:
            max_pwm = pwm
        if max_temperature is None:
            max_temperature = temperature
        if temperature > max_temperature:
            max_temperature = temperature
    gpx_rows = [
        '<?xml version="1.0"?>',
        '<gpx version="1.1"',
        ' creator="CSV to GPX - https://app.alexandersobyanin.ru/csv_to_gpx/"',
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        ' xmlns="http://www.topografix.com/GPX/1/1"',
        ' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">',
        ' <metadata>',
        f'  <link href="https://app.alexandersobyanin.ru/csv_to_gpx/">',
        f'   <text>CSV to GPX</text>',
        f'  </link>',
        f'  <time>{start_time.isoformat()}</time>',
        f'  <bounds minlat="{min_lat}" minlon="{min_lon}" maxlat="{max_lat}" maxlon="{max_lon}"/>',
        ' </metadata>',
        ' <trk>',
        f'  <name>{file.filename.replace(".csv", "")} speed={max_gps_speed} pwm={max_pwm} temperature={max_temperature}</name>',
        '  <trkseg>',
    ]
    file.seek(0)
    csv_reader = csv.DictReader(codecs.iterdecode(file, 'utf-8'))
    for row in csv_reader:
        latitude = row['latitude']
        longitude = row['longitude']
        gps_speed = row['gps_speed']
        altitude = row['gps_alt']
        gps_time = datetime.datetime.strptime(f"{row['date']} {row['time']}", '%Y-%m-%d %H:%M:%S.%f')
        gpx_rows.extend([
            f'  <trkpt lat="{latitude}" lon="{longitude}">',
            f'   <speed>{gps_speed}</speed>',
            f'   <ele>{altitude}</ele>',
            f'   <time>{gps_time}</time>',
            '  </trkpt>'
        ])
    gpx_rows.extend([
        '  </trkseg>',
        ' </trk>',
        '</gpx>'
    ])
    return csv_to_gpx.response_class(
        generate_gpx(),
        mimetype='application/gpx+xml',
        headers={'Content-Disposition': f'attachment; filename={file.filename.replace(".csv", ".gpx")}'}
    )
