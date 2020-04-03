# -*- coding: utf-8 -*-
"""
- flask 선언 및 옵션 지정, Route 전처리, 후처리를 여기서 처리
- 세션이나 쿠키, 해더 키 선언 정도 추가 필요
"""
from flask import Flask, g, render_template
import logging
app = Flask(__name__)

# 라이브러리 Path 등록 --------------------------------------------
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# app config set -------------------------------------------------
app.debug = True	# Detail Debug
app.jinja_env.trim_blocks = True
app.config['TEMPLATES_AUTO_RELOAD']=True

# logging --------------------------------------------------------
# route 전/후 처리에서 사용 될 app전용 로거
from _lib._h_logger_v2 import CustomLogger
app.logger.addHandler(CustomLogger('flask'))
# app.logger.info("Flask 모듈 전용 로거 장착 및 실행 예시")
app.logger.setLevel(logging.CRITICAL)

# app route 전/후 처리 --------------------------------------------
# 매 요청마다 실행
@app.before_request
def before_request():
	g.page_title = "NTREX 장부 ERP"   # 브라우저 탭 상단 TITLE 기본 값
	# print("매 요청마다 실행")

"""
@app.before_first_request
def before_first_request():
	print("앱 기동하고 맨처음 요청만 응답")

@app.after_request
def after_request(response):
	print("매 요청 처리되고 나서 실행")
	return response

@app.teardown_request
def teardown_request(exception):
	return "브라우저가 응답하고 실행"

@app.teardown_appcontext
def teardown_appcontext(exception):
	print("HTTP 요청 애플리케이션 컨텍스트가 종료될때 실행")
"""

# 404 Not Found 정의
@app.errorhandler(404)
def not_found(e):
	# defining function
	data = dict(e=404)
	return render_template("exception/404.html", data=data)

# # 500 Server Internal Error 정의
# @app.errorhandler(500)
# def handle_500(e):
#     original = getattr(e, "original_exception", None)
#
#     if original is None:
#         # direct 500 error, such as abort(500)
#         return render_template("500.html"), 500
#
#     # wrapped unhandled error
#     return render_template("500.html", e=original), 500

# import traceback
# from werkzeug.exceptions import HTTPException
# @app.errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     if isinstance(e, HTTPException):
#         return e
#
#     # now you're handling non-HTTP exceptions only
#     # traceback.print_exc(file=sys.stdout)
#     # exc_type, exc_value, exc_traceback = sys.exc_info()
#     data = dict(e=e)
#     return render_template("exception/500.html", data=data), 500


# Route Load -----------------------------------------------------
from . import route
