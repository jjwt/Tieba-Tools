#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, \
    url_for, make_response, current_app
from ..utils import reg_check_username, reg_check_password, \
    ERR_MSG, gen_pwd_hash
from ..sql_utils import sql_add_user, add_login_err, \
    check_login_err_count, add_token
from ..models import User, db, PersisToken
from sqlalchemy import and_

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def page_register(**kwargs):
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get('username')
    password = request.form.get('password')
    passwordag = request.form.get('passwordag')

    if not (reg_check_username(username) and reg_check_password(password)):
        data_dict = {
            'err': ERR_MSG['4'],
            'username': username,
            'password': password,
            'passwordag': passwordag,
        }
        return render_template('register.html', **data_dict)
    e = sql_add_user(username, password)
    if e == '0':
        return add_token(username)
    if e not in ['1', '2', '5']:
        e = '5'

    data_dict = {
        'err': ERR_MSG[e],
        'username': username,
        'password': password,
        'passwordag': passwordag,
    }
    return render_template('register.html', **data_dict)


@auth.route('/login', methods=['GET', 'POST'])
def page_login():
    if request.method == 'GET':
        return render_template('login.html')

    if not check_login_err_count():
        return render_template('login.html', err=ERR_MSG['13'])

    username = request.form.get('username')
    password = request.form.get('password')
    result = User.query.filter(User.username == username).all()
    if not result:
        current_app.logger.debug('user not found in db')
        data_dict = {
            'err': ERR_MSG['3'],
            'username': username,
            'password': password,
        }
        add_login_err()
        return render_template('login.html', **data_dict)
    user = result[0]
    if gen_pwd_hash(password, user.salt) != user.pwd_hash:
        current_app.logger.debug('wrong password')
        data_dict = {
            'err': ERR_MSG['3'],
            'username': username,
            'password': password,
        }
        add_login_err()
        return render_template('login.html', **data_dict)
    if user.banned == 1:
        current_app.logger.debug('user banned')
        return redirect(url_for('auth.page_banned'))
    return add_token(username)


@auth.route('/logout')
def page_logout():
    token = request.cookies.get('token')
    if token:
        t = token.split('s', 1)
        if (len(t) == 2 and t[0].isdigit()):
            user_id, ptoken = t
            user_id = int(user_id)
            PersisToken.query.filter(
                and_(PersisToken.user_id == user_id,
                     PersisToken.token == token)).\
                update({"deleted": 1})
            db.session.commit()

    resp = make_response(redirect(url_for('auth.page_login')))
    resp.set_cookie('token', expires=0)
    return resp


@auth.route('/banned')
def page_banned():
    return ERR_MSG['14']
