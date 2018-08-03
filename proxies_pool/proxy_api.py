"""
Author：Alex Yang
Time: 2018-07-31
Target：使用Flask提供外部可访问的接口
Package：flask
"""

from flask import Flask, g
from .db import RedisClient

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return 'Proxy Pool'


@app.route('/random')
def get_random():
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_count():
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()
