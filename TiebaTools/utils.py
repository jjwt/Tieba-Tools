#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import time
from base64 import b64encode
from os import urandom
from flask import jsonify
from hashlib import sha256
import re
from tbtools.client import Client

ERR_MSG = {
    '0': '操作成功!',
    '1': '用户名或密码为空!',
    '2': '用户名已经存在',
    '3': '用户名或密码错误!',
    '4': '用户名或密码格式错误!',
    '5': '操作失败,未知错误!',
    '6': '您无权进行此操作',
    '7': '该用户并不存在',
    '8': '提交参数错误',
    '9': '其他用户已绑定该贴吧用户',
    '10': '该用户bduss已经失效，请重新绑定',
    '11': '获取贴吧列表失败',
    '12': '数据库操作失败，未知错误',
    '13': '登录错误操作次数已达过多，请稍后再试',
    '14': '该用户已被封禁，请与网站管理员联系',
    '15': '已添加到系统任务列表，请稍后查看',
    '16': '已添加到系统任务列表，请勿重复提交',
    '17': '该贴吧用户还未更新贴吧列表或没有关注的吧',
}


def json_err(err_no, **kwargs):
    data_dict = {
        'err_no': err_no,
        'err_msg': ERR_MSG[err_no]
    }
    data_dict.update(**kwargs)
    return jsonify(**data_dict)


def gen_expire_time(lifetime=2592000):
    '''gen expire time, default 30 days
    '''
    return int(time())+lifetime


def gen_token():
    return b64encode(urandom(128)).decode('utf-8')


def gen_salt():
    return b64encode(urandom(64)).decode('utf-8')


def gen_pwd_hash(pwd, salt):
    return sha256((salt+pwd).encode('utf-8')).hexdigest()


def reg_check_username(username):
    if not 4 <= len(username) <= 8:
        return False
    if re.search('\s', username):
        return False
    return True


def reg_check_password(password):
    if not 6 <= len(password) <= 16:
        return False
    has_chr = False
    has_digit = False
    for i in password:
        if re.match('[a-zA-Z]', i):
            has_chr = True
        elif i.isdigit():
            has_digit = True
        else:
            return False
    if has_chr and has_digit:
        return True
    return False


def init_one_client(bduss):
    tc = Client()
    tc.bduss = bduss
    tc.add_value2cookie('BDUSS', bduss)
    tc.get_tbs()
    return tc
