from flask import render_template

def index():
	data = dict(val='Test Value')
	return render_template('/main/index.html', data=data)