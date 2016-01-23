#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from TiebaTools import app, db
with app.app_context():
    db.create_all()
app.run()
