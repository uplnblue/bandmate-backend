import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    CLIENT_ID = 'f9481f85fd6c4313a7eb8594f8e3a691'
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
