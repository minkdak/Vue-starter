# -*- coding: utf-8 -*-
"""
* 각 URL에 맞는 라우팅 처리
* 각 URL에 해당되는 컨트롤러 해당 부분은 Controllers 폴더 아래에 모듈로 작업
* 각 URL에 해당되는 컨트롤러가 Controllers/__init__.py에서 __all__에 명시되지 않은 경우 여기서 에러가 발생한다.
* 자동 선언이 어려웠던 관계로 app.add_url_rule()로 각각 선언이 필요
"""
from . import app
from .Controllers import *  # API별 모듈 로드 : 해당 디렉토리 내의 __init__.py에서  자동으로 지정 해줌

# / 접근 만들기
app.add_url_rule('/', None, main.index)

# Route A111 지정
# app.add_url_rule('/A111_01', None, A111.A111_01)    # PyMySQL Sucess
# app.add_url_rule('/A111_02', None, A111.A111_02)    # PyMySQL Error
# app.add_url_rule('/A111_03', None, A111.A111_03)    # PyMySQL & Redis


# 로그인
# app.add_url_rule('/NSB010100', None, NSB01.NSB010100)    # 로그인 폼
