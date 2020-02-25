#coding=utf-8

import json
import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_celery import Celery

db = SQLAlchemy()

migrate = Migrate(db=db)

celery = Celery()


def to_json_ext(inst, cls):
    """
    Jsonify the sqlalchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        
        if isinstance(v, datetime.date):
            v = v.strftime('%Y-%m-%d %H:%M:%S')

        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d
