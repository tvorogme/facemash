#!/usr/bin/env python
# coding=utf-8
import sqlite3
from os import listdir
from os.path import isfile, join

class DataUtils:
    def update_girs(self):
        filenames_in_data = self.cursor.execute('SELECT filename FROM girls').fetchall()
        files = [f for f in listdir('data') if isfile(join('data', f))]

        for filename in files:
            if (filename,) not in filenames_in_data:
                self.cursor.execute('''INSERT INTO girls VALUES (?, 0)''', (filename,))
                print('New girl %s' % filename)
        self.conn.commit()

    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()

        try:
            print('Create table.')
            self.cursor.execute('''CREATE TABLE girls (filename text, rating INT)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print('Table already created.')
            pass

        self.update_girs()

    def get_random_girl(self):
        return self.cursor.execute('''SELECT * FROM girls ORDER BY RANDOM() LIMIT 1''').fetchone()

    def get_girl(self, girl_name):
        return self.cursor.execute('''SELECT * FROM girls WHERE filename=? ''', (girl_name,)).fetchone()

    @staticmethod
    def expected_value(first, second):
        return 1/1+10*((first-second)/400)

    def update_rating(self, girls):
        # Dict to array
        girls = list(map(lambda key: (key, girls[key]), girls))

        e = self.expected_value(girls[0][1], girls[1][1])

        for girl in girls:
            girl_score = self.get_girl(girl[0])[1]

            if girl_score == 0:
                k = 40
            elif girl_score < 2400:
                k = 20
            elif girl_score > 2400:
                k = 10

            new_rating = girl_score + k * (girl[1] - e)
            self.cursor.execute('''UPDATE girls SET rating=? WHERE filename=? ''', (new_rating, girl[0]))

        self.conn.commit()