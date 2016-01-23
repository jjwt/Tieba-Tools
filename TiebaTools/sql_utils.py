#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import User, db, PersisToken, LoginError
from sqlalchemy import and_
from flask import make_response, redirect, request, url_for, \
    current_app
from .utils import gen_salt, gen_pwd_hash
import time
Error_Limit = 3


def sql_add_user(username, password, role=1, banned=0):
    result = User.query.filter(User.username == username).count()
    if result > 0:
        current_app.logger.debug('user find int db')
        return '2'
    try:
        user = User(username=username, password=password,
                    role=role, banned=banned)
        current_app.logger.debug('a user created')
        db.session.add(user)
        db.session.commit()
        current_app.logger.debug('a user added into db')
        return '0'
    except:
        return '5'


def add_token(username):
    '''gen a token for user, add it into db, and
    redirect to main page.
    '''
    current_app.logger.debug('get user_id')
    user_id = User.query.filter(User.username == username).all()[0].user_id
    token = PersisToken(user_id=user_id)
    current_app.logger.debug('add token')
    db.session.add(token)
    db.session.commit()
    current_app.logger.debug('redirect')
    resp = make_response(redirect(url_for('homepage.page_main')))
    cookie_token = str(user_id)+'s'+token.token
    current_app.logger.debug('cookie_token%s' % cookie_token)
    resp.set_cookie('token', cookie_token, expires=token.expire_time)
    return resp


def add_login_err():
    ip = request.remote_addr
    result = LoginError.query.filter(
        and_(LoginError.ip == ip, LoginError.deleted == 0)).all()
    if result:
        result[0].err_count += 1
        db.session.commit()
    else:
        err = LoginError(ip=ip)
        db.session.add(err)
        db.session.commit()


def check_login_err_count():
    '''check if login error count exceeds Error_Limit
    '''
    ip = request.remote_addr
    result = LoginError.query.filter(
        and_(LoginError.ip == ip,
             LoginError.err_count == Error_Limit,
             LoginError.deleted == 0)).limit(1).all()
    if result:
        expire_time = result[0].expire_time
        if time.time() > expire_time:
            result[0].deleted = 1
            db.session.commit()
            return True
        return False
    return True
