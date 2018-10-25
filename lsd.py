#!python3

from flask import Flask

app = Flask(__name__)


@app.route('/')
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


@app.route('/health.php')
def health():
    return '1'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
