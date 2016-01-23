#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from .utils import gen_expire_time, gen_salt, gen_pwd_hash, \
    gen_token

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    pwd_hash = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    role = db.Column(db.Integer, default=1)
    banned = db.Column(db.Integer, default=0)

    def __init__(self, username, password, role=1, banned=0):
        self.username = username
        self.salt = gen_salt()
        self.pwd_hash = gen_pwd_hash(password, self.salt)
        self.role = role
        self.banned = banned

    def __repr__(self, ):
        return '<User %r>' % self.username


class PersisToken(db.Model):
    __tablename__ = 'persis_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(128), default=gen_token)
    expire_time = db.Column(db.Integer, default=gen_expire_time)
    deleted = db.Column(db.Integer, default=0)


class LoginError(db.Model):
    __tablename__ = 'login_err'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20), nullable=False)
    err_count = db.Column(db.Integer, default=1)
    expire_time = db.Column(db.Integer, default=gen_expire_time)
    deleted = db.Column(db.Integer, default=0)


class Tbuser(db.Model):
    __tablename__ = 'user_tbuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    tbuser_name = db.Column(db.String(30), nullable=False)
    bduss = db.Column(db.String(60), nullable=False)
    bduss_ok = db.Column(db.Integer, default=1)


class TiebaList(db.Model):
    __tablename__ = 'tieba_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tbuser_name = db.Column(db.String(30), nullable=False)
    tb_name = db.Column(db.String(30), nullable=False)
    tb_id = db.Column(db.String(30), nullable=False)
    signed = db.Column(db.Integer, default=0)


class SignRecords(db.Model):
    __tablename__ = 'sign_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tbuser_name = db.Column(db.String(30), nullable=False)
    tb_name = db.Column(db.String(30), nullable=False)
    sign_date = db.Column(db.String(8), nullable=False)
    err_no = db.Column(db.Integer, default=0)


class TodoUpdatetblist(db.Model):
    __tablename__ = 'todo_updatetblist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    finish_date = db.Column(db.String(8), nullable=False)


class TodoDelcookiefile(db.Model):
    __tablename__ = 'todo_delcookiefile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(30), nullable=False)
    expire_time = db.Column(db.Integer, default=lambda: gen_expire_time(900))
    deleted = db.Column(db.Integer, default=0)
