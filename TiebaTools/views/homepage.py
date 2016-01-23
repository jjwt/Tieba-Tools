#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, current_app
from ..decorators import de_check_token
from math import ceil
from ..models import Tbuser

homepage = Blueprint('homepage', __name__)


def atry():
    return 'hello world'


@homepage.route('/')
@de_check_token
def page_main(**kwargs):
    role = kwargs.get('role')
    if int(role) == 1:
        current_app.logger.debug('role is common user, turn to page_user_com')
        return page_user_com(**kwargs)

    '''
    if int(role) == 0:
        return page_user_admin(**kwargs)
    '''


def page_user_com(tmpfile='layout.html', **kwargs):
    user_id = kwargs.get('user_id')
    NUM_PER_TBUSERS = current_app.config.get('NUM_PER_TBUSERS', 15)
    count_tbusers = Tbuser.query.filter(Tbuser.user_id == user_id).count()
    max_pn_tbusers = ceil(count_tbusers / NUM_PER_TBUSERS)
    pn = kwargs.get("pn", 1)
    if max_pn_tbusers == 0:
        tbusers = []
    else:
        tbusers = Tbuser.query.filter(Tbuser.user_id == user_id) \
            .limit(NUM_PER_TBUSERS) \
            .offset((int(pn)-1)*NUM_PER_TBUSERS) \
            .all()
    data_dict = {
        'max_pn_tbusers': max_pn_tbusers,
        'tbusers': tbusers,
        'pn_tbusers': int(pn),
        'count_tbusers': count_tbusers,
        'num_per_tbusers': NUM_PER_TBUSERS,
    }
    data_dict.update(**kwargs)
    # return 'hello world'
    return render_template(tmpfile, **data_dict)
