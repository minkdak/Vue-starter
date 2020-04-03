# -*- coding: utf-8 -*-
import os, time
# import gzip   # 롤오버 시 파일 압축할때 필요
import logging
from logging import handlers

# TimedRotatingFileHandler 상속받아 용량, 갯수, 시간에 따라 로그파일을 로테이션 시킴
class CustomLogger(logging.handlers.TimedRotatingFileHandler):
	# 상속을 받았기 때문에 logging 의 옵션을 생성자에서 지정
	def __init__(self, filename, maxBytes=1024 * 1024, backupCount=30, encoding='utf-8', delay=0, when='midnight', interval=1, utc=False):
		# logfile = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), '_logs', f'{filename}.log')
		# 기존 프로젝트 경로에 넣으려고 하니 Text file busy로 에러난다. VM의 공유 디렉토리가 문제 되어 보임
		# 아래와 같이 새로 지정한다.
		logdir = '/Project/_logs/'
		if not os.path.exists(logdir):
			os.makedirs(logdir)
		logfile = os.path.join(logdir, f'{filename}.log')

		# 어짜피 상속관계인데 super()를 사용
		# logging.handlers.TimedRotatingFileHandler.__init__(self, logfile, when, interval, backupCount, encoding, delay, utc)
		# handlerConfig = dict(filename=logfile, when=when, interval=interval, backupCount=backupCount, encoding=encoding, utc=utc, delay=delay)
		# super().__init__(**handlerConfig)
		super().__init__(**dict(
			filename=logfile
			, when=when
			, interval=interval
			, backupCount=backupCount
			, encoding=encoding
			, utc=utc
			, delay=delay
		))

		self.suffix = "%Y-%m-%d"
		self.maxBytes = maxBytes
		self.backupCount = backupCount
		self.propagate = False  # 각각의 logging 모듈이 Root와 연동되므로 전파되지 않도록 False 지정
		customFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s :: %(filename)s(%(lineno)d)')
		self.setFormatter(customFormatter)

	# 시간/용량에 따라 파일을 로테이션 지정
	def shouldRollover(self, record):
		"""
		Determine if rollover should occur.

		Basically, see if the supplied record would cause the file to exceed
		the size limit we have.

		we are also comparing times
		"""
		if self.stream is None:  # delay was set...
			self.stream = self._open()
		if self.maxBytes > 0:  # are we rolling over?
			msg = "%s\n" % self.format(record)
			self.stream.seek(0, 2)  # due to non-posix-compliant Windows feature
			if self.stream.tell() + len(msg) >= self.maxBytes:
				return 1
		t = int(time.time())
		if t >= self.rolloverAt:
			return 1
		# print "No need to rollover: %d, %d" % (t, self.rolloverAt)
		return 0

	# 롤오버시 파일명에 접미사 부여
	def doRollover(self):
		"""
		do a rollover; in this case, a date/time stamp is appended to the filename
		when the rollover happens.  However, you want the file to be named for the
		start of the interval, not the current time.  If there is a backup count,
		then we have to get a list of matching filenames, sort them and remove
		the one with the oldest suffix.
		"""
		if self.stream:
			self.stream.close()
		# get the time that this sequence started at and make it a TimeTuple
		currentTime = int(time.time())
		dstNow = time.localtime(currentTime)[-1]
		t = self.rolloverAt - self.interval
		if self.utc:
			timeTuple = time.gmtime(t)
		else:
			timeTuple = time.localtime(t)
			dstThen = timeTuple[-1]
			if dstNow != dstThen:
				if dstNow:
					addend = 3600
				else:
					addend = -3600
				timeTuple = time.localtime(t + addend)
		dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
		if self.backupCount > 0:
			cnt = 1
			dfn2 = "%s.%03d" % (dfn, cnt)
			while os.path.exists(dfn2):
				dfn2 = "%s.%03d" % (dfn, cnt)
				cnt += 1
			os.rename(self.baseFilename, dfn2)
			for s in self.getFilesToDelete():
				os.remove(s)
		else:
			if os.path.exists(dfn):
				os.remove(dfn)
			os.rename(self.baseFilename, dfn)
		# print "%s -> %s" % (self.baseFilename, dfn)
		self.mode = 'w'
		self.stream = self._open()
		newRolloverAt = self.computeRollover(currentTime)
		while newRolloverAt <= currentTime:
			newRolloverAt = newRolloverAt + self.interval
		# If DST changes and midnight or weekly rollover, adjust for this.
		if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
			dstAtRollover = time.localtime(newRolloverAt)[-1]
			if dstNow != dstAtRollover:
				if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
					addend = -3600
				else:  # DST bows out before next rollover, so we need to add an hour
					addend = 3600
				newRolloverAt += addend
		self.rolloverAt = newRolloverAt

	# 롤오버 할 때 삭제할 파일을 결정
	def getFilesToDelete(self):
		"""
		Determine the files to delete when rolling over.

		More specific than the earlier method, which just used glob.glob().
		"""
		dirName, baseName = os.path.split(self.baseFilename)
		fileNames = os.listdir(dirName)
		result = []
		prefix = baseName + "."
		plen = len(prefix)
		for fileName in fileNames:
			if fileName[:plen] == prefix:
				suffix = fileName[plen:-4]
				if self.extMatch.match(suffix):
					result.append(os.path.join(dirName, fileName))
		result.sort()
		if len(result) < self.backupCount:
			result = []
		else:
			result = result[:len(result) - self.backupCount]
		return result

	# 로그파일 로테이션 발생시 파일을 압축(큰 용량일 경우 부하가 예상되므로 그냥 사용 안함)
	# https://stackoverflow.com/questions/29602352/how-to-mix-logging-handlers-file-timed-and-compress-log-in-the-same-config-f
	# def rotate(self, source, dest):
	# 	""" Compress rotated log file """
	# 	os.rename(source, dest)
	# 	f_in = open(dest, 'rb')
	# 	f_out = gzip.open("%s.gz" % dest, 'wb')
	# 	f_out.writelines(f_in)
	# 	f_out.close()
	# 	f_in.close()
	# 	os.remove(dest)


"""
# app 이외의 커스텀 로그를 남길 때 사용할 로거 생성
# 라이브러리 또는 Router 이후 디버그용 기록 필요시 사용

++++ 사용법 ++++
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), '_lib'))
from _h_logger_v2 import NewLogger
applog = NewLogger('app')._GetLogger()
"""
class NewLogger():
	def __init__(self, nm='', level='DEBUG', outtype=False):
		self.mylog = logging.getLogger(nm)
		self.mylog.setLevel(self._LevelSwitch(level))
		self.mylog.addHandler(CustomLogger(nm))
		self.mylog.propagate = False    # 각각의 logging 모듈이 Root와 연동되므로 전파되지 않도록 False 지정

		# 시스템 출력을 이용하려면(print 기능) logging.StreamHandler()를 핸들러로 추가하면 됨.
		if outtype == True:
			self.mylog.addHandler(logging.StreamHandler())

	# 인자가 잘못 들어왔으면 Default로 logging.DEBUG : DEBUG로 반환
	def _LevelSwitch(self, value):
		return {
			'DEBUG': logging.DEBUG,
			'INFO': logging.INFO,
			'WARNING': logging.WARNING,
			'ERROR': logging.ERROR,
			'CRITICAL': logging.CRITICAL,
		}.get(value, logging.DEBUG)

	def _GetLogger(self):
		return self.mylog