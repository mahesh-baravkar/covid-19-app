import os
import logging
import configparser

def config_from_ini(app, config_file = None, section='flask'):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    logging.debug('Loading Flask configuration from %s' % config_file)
    config = configparser.ConfigParser()
    config.read(config_file)
    flask_config = dict(config.items(section))
    for cfg_key in flask_config:
        app.config[cfg_key.upper()] = flask_config[cfg_key]


