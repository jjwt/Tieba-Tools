#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, \
    request, jsonify, current_app
from ..utils import json_err
from ..models import db, Tbuser, TodoDelcookiefile, \
    TiebaList, SignRecords
from tbtools.client import Client
from sqlalchemy import and_
from ..decorators import de_check_token, de_check_tbuid
from math import ceil

tbuser = Blueprint('tbuser', __name__)


@tbuser.route('/getvercode', methods=['GET', 'POST'])
@de_check_token
def get_vcode(**kwargs):
    tbuser_name = request.form.get('tbuser_name')
    if not tbuser_name:
        return json_err('1')
    b = Client(cookiefile='temp_cookie_'+tbuser_name)
    vcodestr = b.get_vcodestr(tbuser_name)
    if vcodestr:
        result = TodoDelcookiefile.query.filter(
            and_(TodoDelcookiefile.filename == b.cookiefile,
                 TodoDelcookiefile.deleted == 0)).count()
        if result == 0:
            db.session.add(TodoDelcookiefile(filename=b.cookiefile))
            db.session.commit()
        return json_err('0', vcodestr=vcodestr)
    else:
        return json_err('5')


@tbuser.route('/add', methods=['POST'])
@de_check_token
def add_tbuser(**kwargs):
    tbuser_name = request.form.get('tbuser_name')
    tbuser_pw = request.form.get('tbuser_pw')
    verifycode = request.form.get('verifycode')
    vcodestr = request.form.get('vcodestr')
    if not all((tbuser_name, tbuser_pw, verifycode, vcodestr),):
        current_app.logger.debug('at least one input is blank !')
        return json_err('8')
    result = Tbuser.query.filter(Tbuser.tbuser_name == tbuser_name).count()
    if result > 0:
        return json_err('2')
    cookiefile = 'temp_cookie_'+tbuser_name
    b = Client(cookiefile=cookiefile)
    bduss = b.get_bduss(tbuser_name, tbuser_pw, verifycode, vcodestr)
    if not bduss:
        return json_err('5')
    try:
        user_id = int(kwargs.get('user_id'))
        tb_user = Tbuser(user_id=user_id, tbuser_name=tbuser_name,
                         bduss=bduss)
        db.session.add(tb_user)
        db.session.commit()
        return json_err('0', tbuser_id=tb_user.id, tbuser_name=tbuser_name)
    except:
        return json_err('5')


@tbuser.route('/del', methods=['POST'])
@de_check_token
@de_check_tbuid
def del_tbuser(**kwargs):
    tbuser_id = int(kwargs.get('tbuser_id'))
    tbuser_name = kwargs.get('tbuser_name')
    user_id = int(kwargs.get('user_id'))
    try:
        Tbuser.query.filter(
            and_(Tbuser.id == tbuser_id,
                 Tbuser.user_id == user_id)).delete()
        TiebaList.query.filter(TiebaList.tbuser_name == tbuser_name).delete()
        SignRecords.query.filter(
            SignRecords.tbuser_name == tbuser_name).delete()
        db.session.commit()
        return json_err('0')
    except:
        return json_err('12')


@tbuser.route('/get', methods=['POST'])
@de_check_token
def get_tbuser(**kwargs):
    user_id = kwargs.get('user_id')
    NUM_PER_TBUSERS = current_app.config.get('NUM_PER_TBUSERS', 15)
    count_tbusers = Tbuser.query.filter(
        Tbuser.user_id == user_id).count()
    max_pn_tbusers = ceil(count_tbusers / NUM_PER_TBUSERS)
    pn = min(int(request.form.get("pn", 1)), max_pn_tbusers)
    if max_pn_tbusers == 0:
        tbusers = []
    else:
        result = Tbuser.query.filter(Tbuser.user_id == user_id) \
            .limit(NUM_PER_TBUSERS) \
            .offset((int(pn)-1)*NUM_PER_TBUSERS) \
            .all()
        tbusers = [{
            'id': u.id,
            'tbuser_name': u.tbuser_name,
            'bduss': u.bduss,
            'bduss_ok': u.bduss_ok
        } for u in result]
    data_dict = {
        'max_pn_tbusers': max_pn_tbusers,
        'tbusers': tbusers,
        'pn_tbusers': int(pn),
        'count_tbusers': count_tbusers,
        'num_per_tbusers': NUM_PER_TBUSERS,
    }
    return jsonify(**data_dict)
