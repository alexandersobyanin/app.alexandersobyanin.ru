#!python3
import os
import json


class SEO(object):
    yandex = None
    google = None

    def __init__(self):
        seo = json.loads(os.environ.get('SEO', {}))
        self.yandex = seo.get('yandex', {})
        self.google = seo.get('google', {})
