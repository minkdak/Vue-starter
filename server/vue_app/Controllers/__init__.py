# -*- coding: utf-8 -*-
"""
* 외부에서 현재 폴더를 통째로 로드하는 경우
	사용법은 'from Controllers import *' 지정이 가능하다
	다만 모듈명이 정해지지 않았기에 사용시 Error를 배출한다.

* Error를 만들지 않기 위해
	해당 폴더 안의 __init__.py에 __all__에 필요한 모듈만 지정하면 된다.
	이때 값은 list로 지정해야 함

* 아래 샘플은 'A'로 시작 하는 모듈 파일명 일 때만 자동 포함 되도록 지정했다.
	실제 운영시 화면장표 ID의 공통 Prefix 값으로 변경필요
ex)
Type 1 : 직접 타이핑
	__all__ = ['A111', 'A112']
Type 2 : 파일 목록을 획득하여 루프를 돌면서 list 생성 후 __all__에 대입
	load_list = []  # 기본 import 될 module 파일 이름(확장자 제외)

	import os, re   # os : 파일목록 조회용, re : 정규식
	for file in os.listdir('./flaskapp/Controllers'):
		if file.endswith(".py"):
			if re.search('^A', file):
				load_list.append(os.path.splitext(file)[0])

	__all__ = load_list
Type 3 : Type 2를 한줄로 표현(현재 사용 방법)
	import os, re
	__all__ = [os.path.splitext(file)[0] for file in os.listdir('./nsb_web/Controllers') if file.endswith(".py") and re.search('^A', file)]
"""

# __conf, __lib path 자동 지정(Controllers 내의 모든 모듈에서 __conf.컨피그명, __lib.라이브러리명 으로 from import 사용
import os, re, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

# 지정 문자로 시작되는 모듈 명 수집(지정된 Module Name Prefix로 수집)
from _conf.nsb_config import controller_prefix  # Controllers 에서 읽어 들일 모듈의 접두사(리스트로 지정 되어 있음)
alllist = ['main']  # main 을 기본을 지정
for c_prefix in controller_prefix:
	alllist.extend([os.path.splitext(file)[0] for file in os.listdir('./vue_app/Controllers') if file.endswith(".py") and re.search('^'+c_prefix, file)])

# 자동 로드할 모듈 명 지정
__all__ = alllist

# 사용된 변수 삭제
del alllist
