#!/usr/bin/env python
# coding=utf-8
from flask import Flask, render_template, request, redirect
from datautils import DataUtils

du = DataUtils()
app = Flask(__name__, static_folder='data', static_url_path='/images')


@app.route('/')
def index():
    girl_first = du.get_random_girl()
    girl_second = du.get_same_size_girl(girl_first[3], girl_first[4])

    if girl_first == girl_second:
        girl_second = du.get_random_girl()

    try:
        girl_winner = request.args.get('girl_first')
        girl_looser = request.args.get('girl_second')
        du.update_rating({girl_winner: 1, girl_looser: 0})
        redirect('/')
    except IndexError:
        pass

    return render_template('index.html', girl_first=girl_first, girl_second=girl_second)


@app.route('/top_100')
def top_hindret():
    return render_template('top_100.html', girls=du.get_top())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
