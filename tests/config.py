""" Author: Philipp Steinrötter (steinroe) """

import configparser

class MyParser(configparser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

def get_config():
    config = MyParser()
    config.read('config.ini')
    return config.as_dict()
