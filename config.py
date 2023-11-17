import os

class Config(object):
    """
    A class config for flask application
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///tracker.db')
    SECRET_KEY = 'EBMkRjoWquXfbO9F7gUChudYmO/FW66HAjuDOnyb0CA='