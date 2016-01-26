#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from TiebaTools import app, db
from TiebaTools.tasks import daily_sign
with app.app_context():
    db.create_all()

daily_sign.delay()
app.run()
