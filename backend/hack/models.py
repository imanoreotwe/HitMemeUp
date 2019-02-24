from sqlalchemy import Column, Integer, String
from flask import jsonify, Flask
import bcrypt
import json
import jwt
import datetime

from hack.db import Base

class Photo(Base):
    __tablename__ = 'Photos'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    hash = Column(String(255), unique=True)
    location = Column(String(255), unique=True)
    user_fk = Column(Integer, unique=False)
    access = Column(Integer, unique=False)

    def __init__(self, id=None, name=None, hash=None, location=None, access=None, user_fk=None):
        self.id = id
        self.name = name
        self.hash = hash
        self.location = location
        self.user_fk = user_fk
        self.access = access

    def jsonize(self):
        return {'id': self.id,
                'name': self.name,
                'hash': self.hash,
                'user_fk': self.user_fk,
                'access': self.access }

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(64), unique=False)

    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode(), salt)

    def check(self, password):
        if bcrypt.hashpw(password.encode(), self.password.encode()) == self.password.encode():
            return True
        return False

    def encode_token(self, key):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_token(auth_token, key):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def jsonize(self):
       return {'id': self.id,
                'username': self.username,
                'password': self.password}
