# -*- coding: utf-8 -*-
# 레디스 접속 객체를 외부 핸들러로 재정의

# DB, Redis 접속 Config 로드
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from _conf.nsb_config import cache_m_cfg, logname
from _lib._h_logger_v2 import NewLogger
redislog = NewLogger(logname.setdefault('redis', 'app'))._GetLogger()

# Redis 모듈
import redis

# Redis 을 이용한 커스텀 클래스로 작업
class CacheRedis():
	hash_nm = 'socket_hash' # Push 프로젝트에서 사용되는 key name
	def __init__(self):
		try:
			self.cache = redis.StrictRedis(**cache_m_cfg, db=0)
		except redis.ConnectionError as e:
			redislog.error("redis connect fail", e)
			self.cache = False

	def __del__(self):
		if not self.cache:
			self.cache.close()

	def GetQueueObj(self):
		return self.cache, self.hash_nm

	def GetCache(self):
		return self.cache

if __name__ == '__main__':
	r, qnm = CacheRedis().getObj()
	# print(qnm, r.keys('*').decode('utf-8'))
	for key in r.scan_iter():
		print( key.decode('utf-8') )
	print(qnm)