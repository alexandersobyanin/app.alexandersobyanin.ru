#!python3

from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    html = '''<html>
<head>
    <meta name="yandex-verification" content="f988d40377d2dd67" />
    <style>
    * {
        color: white;
        background-color: black;
    }
    </style>
</head>
<body>
<h1>LSD Local Server Dedicated</h1>
</body>
</html>'''
    return html


@app.route('/health.php', methods=['GET'])
@cross_origin(origins=['https://alexandersobyanin.ru'], methods=['GET'])
def health():
    return '{"health":1}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
