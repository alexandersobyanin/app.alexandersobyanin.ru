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


environment_variables = {
    'SEO': SEO,
    'YANDEX_METRIKA': os.environ.get('YANDEX_METRIKA'),
    'GOOGLE_ANALYTICS': os.environ.get('GOOGLE_ANALYTICS')
}
