#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, \
    current_app
from ..decorators import de_check_token, de_check_tbuid
from ..models import TiebaList
from ..tasks import update_one_tblist
from ..utils import json_err
from math import ceil

tblist = Blueprint('tblist', __name__)


@tblist.route('/get', methods=['GET', 'POST'])
@de_check_token
@de_check_tbuid
def get_tblist(**kwargs):
    NUM_PER_TBLIST = current_app.config.get('NUM_PER_TBLIST', 15)
    tbuser_name = kwargs.get('tbuser_name')
    count_tblist = TiebaList.query.filter(
        TiebaList.tbuser_name == tbuser_name).count()
    max_pn_tblist = ceil(count_tblist / NUM_PER_TBLIST)
    pn = min(int(request.form.get("pn", 1)), max_pn_tblist)
    if max_pn_tblist == 0:
        tblist = []
    else:
        result = TiebaList.query.filter(
            TiebaList.tbuser_name == tbuser_name) \
            .limit(NUM_PER_TBLIST) \
            .offset((int(pn)-1)*NUM_PER_TBLIST) \
            .all()
        tblist = [{
            'tb_name': u.tb_name,
            'tb_id': u.tb_id,
            'signed': u.signed,
        } for u in result]
    data_dict = {
        'max_pn_tblist': max_pn_tblist,
        'tblist': tblist,
        'pn_tblist': pn,
        'count_tblist': count_tblist,
        'num_per_tblist': NUM_PER_TBLIST,
    }
    return jsonify(**data_dict)


@tblist.route('/update', methods=['POST'])
@de_check_token
@de_check_tbuid
def update_tblist(**kwargs):
    tbuser_name = kwargs.get('tbuser_name')
    update_one_tblist.delay(tbuser_name)
    return json_err('15')
