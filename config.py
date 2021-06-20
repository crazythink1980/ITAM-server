import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

# log dir
log_dir = os.path.join(basedir, os.getenv('LOG_DIR', 'logs'))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///books.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LOG_LEVEL = logging.INFO
    JWT_SECRET_KEY = 'asldfjklasjfkldsjklasjfklasjlakjf'
