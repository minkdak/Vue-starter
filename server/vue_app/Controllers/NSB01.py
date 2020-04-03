from flask import render_template, g

from _lib._h_mysql_v2 import mysqldb
from _lib._h_redis import CacheRedis
from _lib._h_logger_v2 import NewLogger
from _conf.nsb_config import logname
applog = NewLogger(logname.setdefault('app', 'app'))._GetLogger()

import json # Redis 이용시 키값을 생성하거나 파싱하는데 필요

# 로그인
def NSB010100():
	data = dict(title=g.page_title)
	return render_template('NSB01/NSB010100.html', data=data)
