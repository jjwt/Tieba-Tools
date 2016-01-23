#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, \
    current_app
from ..decorators import de_check_token, de_check_tbuid
from ..models import SignRecords, TiebaList
from math import ceil
from ..utils import json_err
from ..tasks import sign_one_tbuser

sign = Blueprint('sign', __name__)


@sign.route('/get', methods=['GET', 'POST'])
@de_check_token
@de_check_tbuid
def get_signrecords(**kwargs):
    NUM_PER_SIGNRECORDS = current_app.config.get('NUM_PER_SIGNRECORDS', 15)
    tbuser_name = kwargs.get('tbuser_name')
    count_signrecords = SignRecords.query.filter(
        SignRecords.tbuser_name == tbuser_name).count()
    max_pn_signrecords = ceil(count_signrecords / NUM_PER_SIGNRECORDS)
    pn = min(int(request.form.get("pn", 1)), max_pn_signrecords)
    if max_pn_signrecords == 0:
        signrecords = []
    else:
        result = SignRecords.query.filter(
            SignRecords.tbuser_name == tbuser_name) \
            .limit(NUM_PER_SIGNRECORDS) \
            .offset((int(pn)-1)*NUM_PER_SIGNRECORDS) \
            .all()
        signrecords = [{
            'tbuser_name': u.tbuser_name,
            'tb_name': u.tb_name,
            'sign_date': u.sign_date,
            'err_no': u.err_no,
        } for u in result]
    data_dict = {
        'max_pn_signrecords': max_pn_signrecords,
        'signrecords': signrecords,
        'pn_signrecords': pn,
        'count_signrecords': count_signrecords,
        'num_per_signrecords': NUM_PER_SIGNRECORDS,
    }
    return jsonify(**data_dict)


@sign.route('/signnow', methods=['POST'])
@de_check_token
@de_check_tbuid
def sign_now(**kwargs):
    tbuser_name = kwargs.get('tbuser_name')
    sign_per_count = current_app.config.get('SIGN_PER_COUNT', 16)
    count_to_sign = TiebaList.query.filter(
        TiebaList.tbuser_name == tbuser_name).count()
    if count_to_sign == 0:
        return json_err('17')
    sign_times = ceil(count_to_sign / sign_per_count)
    for i in range(sign_times):
        sign_one_tbuser.apply_async(args=[tbuser_name], countdown=i)
    return json_err('15', sign_times=sign_times)
