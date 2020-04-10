import sys, os, copy

# 환경변수를 사용하는 방법으로 os 모듈의 getenv 메서드를 사용한다.
# 환경변수로 PYTHON_ENV 값이 설정되지 않은 경우 None(null) 로 반환된다.
# CentOS 환경변수로 등록하기위해서 /etc/profile 파일 하단에
#       export PYTHON_ENV=development 또는 export PYTHON_ENV=production
#       추가 후 재접속후 echo $PYTHON_ENV 하면 입력된 값을 확인할 수 있다.
run_env = os.getenv('PYTHON_ENV') if os.getenv('PYTHON_ENV') != None else 'development'

# Controllers 에서 읽을 모듈명 접두사
controller_prefix = ['NSB']         # 절대 수정하지 말 것
controller_prefix += ['A', 'B','C','vue'] # 테스트 / 기본 템플릿 적용 확인용

# 로그 파일명(dict)
logname = dict(
	db="db",
	redis='redis',
	app='app'
)

# MySQL 접속 설정 항목
db_cfg_bone = {
	"host": "127.0.0.1",
	"port": 3306,
	"db": "디비명",
	"user": "유저",
	"password": "패스워드",
	"charset": "utf8"
}
db_cfg = {}

# Redis
cache_m_cfg_bone = {
	"host": "127.0.0.1",
	"port": 6379
}

# Sockets
socket_cfg_bone = {
	"host": "0.0.0.0",
	"port": 5959
}

if run_env == 'development':
	# MySQL
	db_cfg['nsb'] = copy.deepcopy(db_cfg_bone)
	db_cfg['nsb']['host'] = '127.0.0.1'
	db_cfg['nsb']['database'] = 'prototype_nsb'
	db_cfg['nsb']['user'] = 'nsbuser'
	db_cfg['nsb']['password'] = '1qazxsw2'

	db_cfg['newdm'] = copy.deepcopy(db_cfg_bone)
	db_cfg['newdm']['host'] = '127.0.0.1'
	db_cfg['newdm']['database'] = 'prototype_newdm'
	db_cfg['newdm']['user'] = 'newdmuser'
	db_cfg['newdm']['password'] = '1qazxsw2'

	db_cfg['101c'] = copy.deepcopy(db_cfg_bone)
	db_cfg['101c']['host'] = '127.0.0.1'
	db_cfg['101c']['database'] = 'prototype_101c'
	db_cfg['101c']['user'] = '101cuser'
	db_cfg['101c']['password'] = '1qazxsw2'

	# Redis
	cache_m_cfg = copy.deepcopy(cache_m_cfg_bone)

	# Socket
	socket_cfg = copy.deepcopy(socket_cfg_bone)
elif run_env == 'production':
	# MySQL
	db_cfg['nsb'] = copy.deepcopy(db_cfg_bone)
	db_cfg['nsb']['host'] = '127.0.0.1'
	db_cfg['nsb']['database'] = 'prototype_nsb'
	db_cfg['nsb']['user'] = 'nsbuser'
	db_cfg['nsb']['password'] = '1qazxsw2'

	db_cfg['newdm'] = copy.deepcopy(db_cfg_bone)
	db_cfg['newdm']['host'] = '127.0.0.1'
	db_cfg['newdm']['database'] = 'prototype_newdm'
	db_cfg['newdm']['user'] = 'newdmuser'
	db_cfg['newdm']['password'] = '1qazxsw2'

	db_cfg['101c'] = copy.deepcopy(db_cfg_bone)
	db_cfg['101c']['host'] = '127.0.0.1'
	db_cfg['101c']['database'] = 'prototype_101c'
	db_cfg['101c']['user'] = '101cuser'
	db_cfg['101c']['password'] = '1qazxsw2'

	# Redis
	cache_m_cfg = copy.deepcopy(cache_m_cfg_bone)

	# Socket
	socket_cfg = copy.deepcopy(socket_cfg_bone)
else:
	print("development 또는 production으로 실행해주세요.")
	sys.exit()
