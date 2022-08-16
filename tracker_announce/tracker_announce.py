#!python3
import os
import socket
import urllib.error
import urllib.parse
import urllib.request
from flask import Blueprint
from flask import Response
from flask import request

from environment_variables import environment_variables

tracker_announce = Blueprint('tracker_announce', __name__)

global_context = {}
global_context.update(environment_variables)


@tracker_announce.route('/<path:tracker_path>', methods=['GET'])
def tracker_announce_process_path(tracker_path):
    pass_key = request.args.get('pk')
    if pass_key != os.environ.get('TRACKER_PASS_KEY'):
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
