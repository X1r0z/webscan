# -*- coding:utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template
from json import dumps
from api import WebScan

app = Flask(__name__)
scan = WebScan()

success = None

@app.route('/')
def index():

    global success

    if request.args.get('a'):
        url = request.args.get('site').strip()
        success = scan.get(url)
        return render_template('index.html',url=url,success=success)

    elif request.args.get('b'):
        url = request.args.get('site').strip()
        result = scan.api(url)
        return render_template('index.html',success=success,url=url,result=result)

    else:
        return render_template('index.html')

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/contact')
def contact():

    return render_template('contact.html')

@app.route('/api')
def api():

    if request.args.get('site'):

        url = request.args.get('site')
        result = scan.api(url)
        return dumps(result)

    return render_template('api.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)