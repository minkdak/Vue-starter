from flask import render_template

from _lib._h_mysql_v2 import mysqldb
from _lib._h_redis import CacheRedis
from _lib._h_logger_v2 import NewLogger
from _conf.nsb_config import logname
applog = NewLogger(logname.setdefault('app', 'app'))._GetLogger()

import json # Redis 이용시 키값을 생성하거나 파싱하는데 필요

# DB Select Default
def A111_01():
	db = mysqldb(['nsb'])
	sql = "SELECT * FROM `test` WHERE `idx` < %s"
	rowstate, rows = db.FetchAll('nsb', sql, [20])

	# 에러가 발생한 경우 여기서 중단
	if not rowstate:
		return rows

	"""
	# 메서드 사용 없이 직접 호출 시
	cursor = db.GetCursor('nsb')
	sql = "SELECT * FROM `test` WHERE `idx` < %s"
	rows = []
	try:
		# Read all record
		cursor.execute(sql, [20])
		rows = cursor.fetchall()
	except Exception as e:
		print(e)
	"""
	applog.info("test app response")
	data = dict(title='Test Title', val='Test Value', list=rows)
	return render_template('A111/A111_01.html', data=data)

# DB Select Query Error
def A111_02():
	db = mysqldb(['nsb', 'newdm'])
	sql = "SELECT * FROM `testa` WHERE `idx` < %s"
	rowstate, rows = db.FetchAll('nsb', sql, [20])
	# print(rowstate, rows)
	# print(type(rows))

	if not rowstate:
		applog.debug("여기서 리턴결과 예외 처리")
		data = dict(error=rows)
		return render_template('layout/base_error.html', data=data)

	return render_template('A111/A111_02.html')

# DB & Redis
def A111_03():
	redis = CacheRedis().GetCache()
	if (not redis.exists('tmpjson')):
		dbtype = "MySQL"
		db = mysqldb(['nsb', 'newdm'])
		sql = "SELECT * FROM `test` WHERE `idx` < %s"
		rowstate, rows = db.FetchAll('nsb', sql, [20])

		if not rowstate:
			print("여기서 리턴결과 예외 처리")
			data = dict(error=rows)
			return render_template('layout/base_error.html', data=data)
		josnstr = json.dumps(rows)
		redis.setex('tmpjson', 10, josnstr) # 키 등록 후 10초뒤 자동 삭제, expire 사용 안하려면 set() 사용
	else:
		dbtype = "Redis"
		rowsstr = redis.get('tmpjson')
		rows = json.loads(rowsstr)

	return render_template('A111/A111_03.html', data=dict(list=rows, dbtype=dbtype))
