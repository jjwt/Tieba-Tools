#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import current_app
from celery import Celery
import json
from .models import db, TodoDelcookiefile, Tbuser, TiebaList, \
    TodoUpdatetblist, SignRecords
import time
from sqlalchemy import and_
import os
from threading import Thread
from .utils import init_one_client


cel = Celery()


@cel.task(name='TiebaTools.tasks.del_cookiefile')
def del_cookiefile():
    '''clear expired cookiefile if exists'''
    result = TodoDelcookiefile.query.filter(
        and_(TodoDelcookiefile.expire_time <= int(time.time()),
             TodoDelcookiefile.deleted == 0)).all()
    if not result:
        return json.dumps({'result': 'none cookiefile to del!'})
    print(result[0].filename)
    dirname = os.path.dirname
    parent_dir = dirname(dirname(__file__))
    for f in result:
        os.remove(os.path.join(parent_dir, f.filename))
        f.deleted = 1
    db.session.commit()
    return json.dumps({'result': 'del cookiefile successfully!'})


def update_tblist(tbusers, thread_count=None):
    '''update tblist of tbusers. tbusers must be a list of Tbuser models.
    '''
    clients = {}
    tblist_pages = []
    tblists = {}
    thread_count = thread_count or \
        current_app.config.get('UPDATE_TBLIST_THREAD_COUNT', 8)
    for u in tbusers:
        tc = init_one_client(u.bduss)
        clients[u.tbuser_name] = tc
        tblist_pages.append((u.tbuser_name, tc.get_tblist_pagecount(),))
        tblists[u.tbuser_name] = []

    def subthread(clients, tblist_pages, tblists):
        while len(tblist_pages) > 0:
            tbuser_name, cur_pagenumber = tblist_pages[0]
            if cur_pagenumber == 1:
                tblist_pages.pop()
            else:
                tblist_pages[0][1] -= 1
            tblist = clients[tbuser_name].get_tblist_bypage(cur_pagenumber)
            tblists[tbuser_name] += tblist

    ps = [Thread(target=subthread, args=(clients, tblist_pages, tblists))
          for i in range(thread_count)]
    for p in ps:
        p.start()
    for p in ps:
        p.join()

    current_app.logger.debug(tblists)
    TiebaList.query.filter(
        TiebaList.tbuser_name.in_(list(tblists.keys()))) \
        .delete(synchronize_session=False)
    db.session.expire_all()
    db.session.commit()
    tblists2db = []
    for tbuser_name, v in tblists.items():
        for tb_id, tb_name in v:
            tblists2db.append(TiebaList(tbuser_name=tbuser_name,
                                        tb_name=tb_name, tb_id=tb_id))

    db.session.add_all(tblists2db)
    db.session.commit()


@cel.task(name='TiebaTools.tasks.update_one_tblist')
def update_one_tblist(tbuser_name):
    '''update tieba list of one tbuser,
    '''
    result = Tbuser.query.filter(
        and_(Tbuser.tbuser_name == tbuser_name,
             Tbuser.bduss_ok == 1)).all()
    update_tblist(result)
    return json.dumps({'result': 'update tblist of %s finish !' % tbuser_name})


@cel.task(name='TiebaTools.tasks.update_all_tblist')
def update_all_tblist():
    '''update tieba list of all tbuser,
    done on start of app or every day after check if done.
    '''
    current_app.logger.debug('update_all_tblist task starts !')
    cur_day = time.strftime('%Y%m%d')
    result = TodoUpdatetblist.query.filter(
        TodoUpdatetblist.finish_date == cur_day).count()
    if result == 1:
        return json.dumps({'result': 'update_all_tblist has done before !'})
    result = Tbuser.query.filter(
        Tbuser.bduss_ok == 1).all()
    if len(result) == 0:
        db.session.add(TodoUpdatetblist(finish_date=cur_day))
        db.session.commit()
        return json.dumps({'result': 'no available tbuser to update tblist !'})
    update_tblist(result)
    db.session.add(TodoUpdatetblist(finish_date=cur_day))
    db.session.commit()
    return json.dumps({'result': 'update_all_tblist finish !'})


def sign_tbuser(tblists, thread_count=None):
    '''sign tblist of tblists and add sign records into database.
    Each member of tblists must be a tuple or list
    in pattern as (tbuser_name, bduss, tb_id, tb_name)
    '''
    clients = {}
    signrecords = []
    cur_day = time.strftime('%Y%m%d')
    if thread_count is None:
        thread_count = current_app.config.get('SIGN_THREAD_COUNT', 8)
    for t in tblists:
        if not t[0] in clients:
            clients[t[0]] = init_one_client(t[1])

    def subthread(clients, signrecords, tblists, sign_date):
        while len(tblists) > 0:
            tbuser_name, bduss, tb_id, tb_name = tblists.pop(0)
            err_no = clients[tbuser_name].sign_single(tb_id, tb_name)['err_no']
            signrecords.append(
                SignRecords(
                    tbuser_name=tbuser_name,
                    tb_name=tb_name,
                    sign_date=cur_day,
                    err_no=err_no,
                ))

    ps = [Thread(target=subthread,
                 args=(clients, signrecords, tblists, cur_day))
          for i in range(thread_count)]
    for p in ps:
        p.start()
    for p in ps:
        p.join()

    db.session.add_all(signrecords)
    db.session.commit()


@cel.task(name='TiebaTools.tasks.sign_all_tbuser')
def sign_all_tbuser(sign_per_count=None):
    '''sign tiebas of all tbusers, sign_per_count every time,
    used for daily sign task'''
    if sign_per_count is None:
        sign_per_count = current_app.config.get('SIGN_PER_COUNT', 16)
    tblist = TiebaList.query \
        .join(Tbuser, TiebaList.tbuser_name == Tbuser.tbuser_name) \
        .add_columns(
            Tbuser.tbuser_name,
            Tbuser.bduss,
            TiebaList.tb_id,
            TiebaList.tb_name) \
        .filter(TiebaList.signed == 0) \
        .limit(sign_per_count).all()
    if len(tblist) == 0:
        return json.dumps({'result': 'none TiebaList to sign !'})
    sign_tbuser(tblist)
    TiebaList.query.filter(
        TiebaList.signed == 0).limit(sign_per_count).update(
            dict(signed=1))
    db.session.commit()
    return json.dumps({'result': 'sign all tblist finish a loop !'})


@cel.task(name='TiebaTools.tasks.sign_one_tbuser')
def sign_one_tbuser(tbuser_name, sign_per_count=None):
    if sign_per_count is None:
        sign_per_count = current_app.config.get('SIGN_PER_COUNT', 16)
    tblist = TiebaList.query \
        .join(Tbuser, TiebaList.tbuser_name == Tbuser.tbuser_name) \
        .add_columns(
            Tbuser.tbuser_name,
            Tbuser.bduss,
            TiebaList.tb_id,
            TiebaList.tb_name) \
        .filter(
            and_(TiebaList.tbuser_name == tbuser_name,
                 TiebaList.signed == 0)) \
        .limit(sign_per_count).all()
    if len(tblist) == 0:
        return json.dumps({'result': 'none TiebaList to sign !'})
    sign_tbuser(tblist)
    TiebaList.query.filter(
        and_(TiebaList.tbuser_name == tbuser_name,
             TiebaList.signed == 0)) \
        .limit(sign_per_count) \
        .update(dict(signed=1))
    db.session.commit()
    return json.dumps({'result': 'sign all tblist finish a loop !'})


@cel.task(name='TiebaTools.tasks.daily_sign')
def daily_sign(sign_per_count=None, sign_time_interval=None):
    update_all_tblist()
    if sign_per_count is None:
        sign_per_count = current_app.config.get('SIGN_PER_COUNT', 16)
    if sign_time_interval is None:
        sign_time_interval = current_app.config.get('SIGN_TIME_INTERVAL', 60)
    while 1:
        tblist = TiebaList.query \
            .join(Tbuser, TiebaList.tbuser_name == Tbuser.tbuser_name) \
            .add_columns(
                Tbuser.tbuser_name,
                Tbuser.bduss,
                TiebaList.tb_id,
                TiebaList.tb_name) \
            .filter(TiebaList.signed == 0) \
            .limit(sign_per_count + 1).all()
        if len(tblist) == 0:
            return json.dumps({'result': 'none TiebaList to sign !'})
        sign_tbuser(tblist[:-1])
        TiebaList.query.filter(
            TiebaList.signed == 0).limit(sign_per_count).update(
                dict(signed=1))
        db.session.commit()
        if len(tblist) <= sign_per_count:
            break
        else:
            time.sleep(sign_time_interval)
    return json.dumps({'result': 'sign all tblist finish a loop !'})
