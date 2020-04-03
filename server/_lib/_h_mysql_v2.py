# -*- coding: utf-8 -*-
"""
# DB Connection Pool 사용자 정의 모듈
# PyMySQL 모듈을 이용해 Class의 생성자(DB접속), 소멸자(DB접속 종료) 이용한 자동 접속, 종료를 하도록 함
# Select 쿼리만 메서드로 구현
# ※ Insert, Update, Delete 쿼리용 commit, rollback을 자동화(메서드 구현) 하려 했으나 쿼리를 여러번 실행하기 때문에 안함

* os.path.join : 경로를 병합하여 새 경로 생성
* os.path.abspath : 특정 경로에 대해 절대 경로 얻기
* os.path.dirname : 경로 중 디렉토리명만 얻기
"""

import os, sys, copy
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 접속 정보
from _conf.nsb_config import db_cfg
dbconfig = db_cfg   # DB 접속 정보

# 커스텀 로거 라이브러리
from _lib._h_logger_v2 import NewLogger
from _conf.nsb_config import logname
dblog = NewLogger(logname.setdefault('db', 'app'))._GetLogger()

# PyMySQL 묘듈 : https://github.com/PyMySQL/PyMySQL
import pymysql.cursors

# PyMySQL 을 이용한 커스텀 클래스로 작업
class mysqldb:
	# 생성자에서 DB Connection 생성
	def __init__(self, types=['nsb']):
		global dbconfig
		self.conn = {}
		self.types = types
		for type in types:
			cfg = copy.deepcopy(dbconfig[type])
			cfg['cursorclass'] = pymysql.cursors.DictCursor
			self.conn[type] = pymysql.connect(**cfg)

	# 열려 있는 DB 구분자별 Close
	def __del__(self):
		# self.conn.keys() 값이 dict_keys 형이라 리스트로 변환 후 출력
		dblog.info("class db close : %s" % list(self.conn.keys()))
		for key in self.conn.keys():
			self.conn[key].close()

	# 지정 type(DB) cursor 반환
	def GetCursor(self, type):
		cursor = self.conn[type].cursor()
		return cursor

	# 모든 types(DB별) cursor 반환
	def GetCursors(self):
		cursors = {}
		for type in self.conn.keys():
			cursors[type] = self.conn[type].cursor()
		return cursors

	# 조회한 레코드를 모두 반환
	def FetchAll(self, type, sql, args):
		try:
			with self.conn[type].cursor() as cursor:
				# Read all record
				cursor.execute(sql, args)
				rows = cursor.fetchall()

				return True, rows
		except Exception as e:
			code, msg = e.args
			output = 'MySQL Error(%d) : %s >>> %s' % (code, msg, cursor._last_executed)
			return False, output

	# 조회한 레코드 중 첫 행만 반환
	def FetchOne(self, type, sql, args):
		try:
			with self.conn[type].cursor() as cursor:
				# Read all record
				cursor.execute(sql, args)
				rows = cursor.fetchone()

				return True, rows
		except Exception as e:
			code, msg = e.args
			output = 'MySQL Error(%d) : %s >>> %s' % (code, msg, cursor._last_executed)
			return False, output

	"""
	# 추후 상세 구현시 아래 내용 기반으로 추가해볼 것.
	def Execute(self, type, sql, args):
		try:
			with self.conn[type].cursor() as cursor:
				# Read all record
				cursor.execute(sql, args)   # 실행하기
				cursor.commit()             # DB에 Complete 하기
				print(cursor.lastrowid)
		except Exception as e:
			raise
		finally:
			return cursor.lastrowid
	"""
