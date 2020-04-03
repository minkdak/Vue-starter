import os, time, datetime
import logging, logging.handlers as handlers

# 스케줄러 모듈
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

# 스케줄러 logger 변경
customFormatter = logging.Formatter('[%(asctime)s - %(levelname)5s] %(message)s')
logfile = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), '_logs', 'schedule_logger.log')
handlerConfig = {'filename':logfile, 'when':'midnight', 'interval':1, 'backupCount':30, 'encoding':'utf-8'}
customFileHandler = handlers.TimedRotatingFileHandler(**handlerConfig)
customFileHandler.suffix = "%Y%m%d"
customFileHandler.setFormatter(customFormatter)
# customStreamHandler = logging.StreamHandler()

slog = logging.getLogger('apscheduler')
slog.setLevel(logging.INFO)
slog.addHandler(customFileHandler)
# slog.addHandler(customStreamHandler)
slog.propagate = False

###############################################################################
class Scheduler():
	# 클래스 생성시 스케쥴러 데몬을 생성합니다.
	def __init__(self):
		self.sched = BackgroundScheduler()
		self.sched.start()
		self.job_id=''

	# 클래스가 종료될때, 모든 job들을 종료시켜줍니다.
	def __del__(self):
		if self.get_jobs() > 0:
			self.shutdown()

	# 모든 job들을 종료시켜주는 함수입니다.
	def shutdown(self):
		if self.get_jobs() > 0:
			self.sched.shutdown()
		else:
			print("Empty Scheduler Job!")

	# 특정 job을 종료시켜줍니다.
	def kill_scheduler(self, job_id):
		# msg = f'{"":><10} "{job_id}" kill cron schedule {"":<<10}'
		# print(msg)
		try:
			self.sched.remove_job(job_id)
		except JobLookupError as err:
			slog.error("fail to stop scheduler: %s" % err)
			return

	def baseJob(self, job_id):
		msg = "[Scheduler]: process_id[%s] - runtime %s" % (job_id, datetime.datetime.now())
		print(msg)
		# slog.info(helloMsg)

	def get_jobs(self):
		# tmpjobs = self.sched.get_jobs()
		# print(type(tmpjobs), len(tmpjobs), tmpjobs)
		return len(self.sched.get_jobs())

	# 스케쥴러입니다. 스케쥴러가 실행되면서 hello를 실행시키는 쓰레드가 생성되어집니다.
	# 그리고 다음 함수는 type 인수 값에 따라 cron과 interval 형식으로 지정할 수 있습니다.
	# 인수값이 cron일 경우, 날짜, 요일, 시간, 분, 초 등의 형식으로 지정하여,
	# 특정 시각에 실행되도록 합니다.(cron과 동일)
	# interval의 경우, 설정된 시간을 간격으로 일정하게 실행실행시킬 수 있습니다.
	# args 의 리스트지정시 해당 Callback 함수의 인자로 정의 된것인지 체크 필수 : argument 에러나서 중지 됨
	def scheduler(self, job_id, cb):
		soption = {'hour':'8-23', 'second':'*/3', 'id':job_id}
		if hasattr(cb, "__call__"):
			self.sched.add_job(cb, 'cron', **soption)
		else:
			soption['args'] = [job_id]
			self.sched.add_job(self.baseJob, 'cron', **soption)

###############################################################################
if __name__=='__main__':
	sid = "Collect_Schedule"
	scheduler = Scheduler()

	# cron 스케쥴러를 실행시키며, job_id는 "test_schedule" 입니다.
	scheduler.scheduler(sid, None)

	count = 0
	while True:
		if count == 10:
			scheduler.kill_scheduler(sid)
		if scheduler.get_jobs() == 0:
			break
		time.sleep(1)
		count += 1
		print(f'{"> Loop tick":->15} : {count}')