# -*- coding: utf-8 -*-
# 장부 ERP - Web 의 Run 파일

from vue_app import app

app.run(host='0.0.0.0', port='2358', threaded=True)