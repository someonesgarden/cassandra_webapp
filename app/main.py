from flask import Flask, Response, request, render_template, redirect, url_for, jsonify, send_from_directory
from flask_wtf import Form
from wtforms import TextField
from flask_bootstrap import Bootstrap
from cassandra.cluster import Cluster
import requests
import hashlib
import logging
from logging.handlers import RotatingFileHandler
import redis
import html
import sys
import os
import re
from flask_socketio import SocketIO, emit, join_room, leave_room, \
      close_room, rooms, disconnect



p = {'cassandra':
        {'ip': '192.168.99.100', 'port': 9042}
}

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "UNIQUE_SALT"
default_name="daisuke nishimura"


# FLASK Socker.IO
app.config['SECRET_KEY'] = 'secret!'
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
thread = None


@socketio.on('connect', namespace='/test')
def test_message():
    app.logger.debug("FLASK socket:CONNECTED!")
    #emit('my response', {'data': 'got it!'})
# FLASK Socker.IO


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def mainpage():

    if request.method == 'POST':
        form = request.form
    elif request.method == 'GET':
        form = request.args
    try:
        p['cassandra']['ip'] = html.escape(form.get('ip'), quote=True)
    except:
        try:
            r = re.compile("http://([a-zA-Z0-9.]+)")
            m = r.search(request.url)
            p['cassandra']['ip'] = m.group(1)
        except:
            app.logger.error('regex error')

    return render_template('index.html', par=p)


@app.route('/cassandra', methods=['GET', 'POST'])
def cassandra():

    if request.method == 'POST':
        form = request.form
    elif request.method == 'GET':
        form = request.args

    try:
        keyspace = html.escape(form.get('keyspace'), quote=True)

    except:
        keyspace = "firsttable"

    # param = json.loads(form.get('param'))

    str1, str2, str3, str4 = "", "", "", ""

    cluster = Cluster(contact_points=[p['cassandra']['ip']], port=p['cassandra']['port'])
    session = cluster.connect()

    try:
        query = "CREATE keyspace "+keyspace+" WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor': 2};"
        result = session.execute(query)

        str1 = keyspace + " CREATED"

    except:
        str1 = keyspace+"ALREAY THERE"

    #session.set_keyspace(keyspace)

    header = '<html><head><title>Cassandra Server</title></head><body>'
    body = '''
    {0}
    {1}
    {2}
    {3}
    '''.format(str1,str2,str3,str4)
    footer = '</body></html>'

    return header + body + footer


@app.route('/monster/<name>')
def get_identicon(name):

    name = html.escape(name, quote=True)
    image = cache.get(name)
    if image is None:

        #print("Cache miss")
        #print ("Cache miss", flush=True)

        r = requests.get('http://dnmonster:8080/monster/'+name+'?size=80')
        image = r.content
        cache.set(name, image)

    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    socketio.run(app, host='0.0.0.0', debug=True)


