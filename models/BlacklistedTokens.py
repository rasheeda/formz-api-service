from sqlalchemy import Column, String, Integer, DateTime
from app import db
import datetime
from app import db
from flask import jsonify

class BlacklistedTokens(db.Model):
    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String(200))
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())

    def __init__(self, token=None):
        self.token = token

    def add(self, token):
        # print(f'--------> in model ----> {token}')

        blacklist = BlacklistedTokens(token, datetime.datetime.now(), datetime.datetime.now())

        print(f'--------> blacklist ----> {blacklist}')
        db.session.add(blacklist)
        db.session.commit()

    def isBlackListedToken(token):
        token = BlacklistedTokens.query.filter_by(token=token).first()

        if token:
            return bool(token)
