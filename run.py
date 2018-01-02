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
    
    elif request.args.get('d'):
        url = request.args.get('site').strip()
        server = scan.server(url)
        return render_template('index.html',success=success,url=url,server=server)

    else:
        return render_template('index.html')

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/contact')
def contact():

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
