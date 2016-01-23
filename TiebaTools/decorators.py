#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''This module collect decorators
used as share utils.
'''
from functools import wraps
from flask import request, redirect, url_for, make_response, current_app
from .models import PersisToken, User, Tbuser
from .models import db
from sqlalchemy import and_
from time import time
from .utils import json_err


def de_check_token(func):
    '''
    1. check if has token in cookies
        if not -> redirect to login page
    2. check if match pattern(user_id,'s',token)
        if not -> redirect to login page, remove token
    3. check if token in database
        if not -> redirect to login page, remove token
    4. check if expired
        if yes -> redirect to login page, remove token
    5. check if banned
        if yes -> redirect to banned page
    6. transform user_id, username, role info of user
        to the func

        output:
            user_id -> int
            username -> str
            role -> int
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_app.logger.debug("de_check_token called by " + func.__name__)
        token = request.cookies.get('token')
        if not token:
            current_app.logger.debug('token not found in cookie')
            return redirect(url_for('auth.page_login'))
        current_app.logger.debug('token found in cookie')
        t = token.split('s', 1)
        if not (len(t) == 2 and t[0].isdigit()):
            current_app.logger.debug('invalid token pattern')
            resp = make_response(redirect(url_for('auth.page_login')))
            resp.set_cookie('token', expires=0)
            return resp
        user_id, ptoken = t
        user_id = int(user_id)
        result = PersisToken.query.filter(
            and_(PersisToken.deleted == 0,
                 PersisToken.user_id == user_id,
                 PersisToken.token == ptoken)).all()
        if not result:
            current_app.logger.debug('persis_token of user not find in db')
            resp = make_response(redirect(url_for('auth.page_login')))
            resp.set_cookie('token', expires=0)
            return resp

        user = result[0]
        if time() > int(user.expire_time):
            user.deleted = 1
            db.session.commit()
            resp = make_response(redirect(url_for('auth.page_login')))
            resp.set_cookie('token', expires=0)
            return resp

        user = User.query.get(user_id)
        current_app.logger.debug('get user from db')
        if user.banned == 1:
            return redirect(url_for('auth.page_banned'))
        data_dict = {
            'user_id': user_id,
            'username': user.username,
            'role': user.role,
        }
        kwargs.update(**data_dict)
        result = func(*args, **kwargs)
        return result
    return wrapper


def de_check_tbuid(func):
    '''
    1. check if has tbuser_id in request
        if not -> return error
    2. check if (user,tbuser) couple in database
        if not -> return error
    3. transform tbuser_id,tbuser_name,bduss,bduss_ok info of user
        to the func
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_app.logger.debug("de_check_tbuid called by " + func.__name__)
        user_id = kwargs.get('user_id')
        tbuser_id = request.form.get('tbuid')
        if not tbuser_id:
            current_app.logger.debug('tbuser_id not given !')
            return json_err('8')
        result = Tbuser.query.filter(
            and_(Tbuser.id == tbuser_id,
                 Tbuser.user_id == user_id)).limit(1).all()
        if not result:
            current_app.logger.debug('tbuser_id invalid !')
            return json_err('8')
        data_dict = {
            'tbuser_name': result[0].tbuser_name,
            'tbuser_id': result[0].id,
            'bduss': result[0].bduss,
            'bduss_ok': result[0].bduss_ok,
        }
        kwargs.update(**data_dict)
        result = func(*args, **kwargs)
        return result
    return wrapper
