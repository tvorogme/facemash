#!/usr/bin/env python
# coding=utf-8
import sqlite3
from os import listdir
from os.path import isfile, join, isdir
from PIL import Image

class DataUtils:
    def update_girs(self):
        filenames_in_data = self.cursor.execute('SELECT filename FROM girls').fetchall()

        for girl in [f for f in listdir('data') if isdir(join('data', f))]:
            files = [f for f in listdir('data/%s' % girl) if isfile(join('data/%s' % girl, f))]
            for filename in files:
                with Image.open('data/{0}/{1}'.format(girl, filename)) as im:
                    width, height = im.size
                if (filename,) not in filenames_in_data:
                    self.cursor.execute('''INSERT INTO girls VALUES (?, 0, ?, ?, ?)''', (filename, girl, width, height))
                    print('New girl %s' % filename)
                    print(width, height)
                    print('-----------------------')

    def __init__(self):
        self.conn = sqlite3.connect('data.db', isolation_level=None, check_same_thread=False)
        self.cursor = self.conn.cursor()

        try:
            print('Create table.')
            self.cursor.execute('''CREATE TABLE girls (filename text, rating INT, pornstarname text, width INT, height INT)''')
        except sqlite3.OperationalError:
            print('Table already created.')
            pass

        self.update_girs()

    def get_random_girl(self):
        return self.cursor.execute('''SELECT * FROM girls ORDER BY RANDOM() LIMIT 1''').fetchone()

    def get_same_size_girl(self, width, height):
        return self.cursor.execute('''SELECT * FROM girls WHERE width=? AND height=? ORDER BY RANDOM() LIMIT 1''', (width, height)).fetchone()

    def get_girl(self, girl_name):
        return self.cursor.execute('''SELECT * FROM girls WHERE filename=? ''', (girl_name,)).fetchone()

    @staticmethod
    def expected_value(first, second):
        return 1/(1+10**((first-second)/400))

    @staticmethod
    def get_koefficient(score):
        if score == 0:
            return 40
        elif score < 2400:
            return 20
        elif score > 2400:
            return 10

    def update_rating(self, girls):
        # Dict to array
        girls = list(map(lambda key: (key, girls[key]), girls))

        girl_first = girls[0]
        girl_second = girls[1]

        # Get rating for first and second girl
        girls_score = (self.get_girl(girl_first[0])[1], self.get_girl(girl_second[0])[1])

        koefficients = (self.get_koefficient(girls_score[0]), self.get_koefficient(girls_score[1]))

        new_rating = (girls_score[0] + koefficients[0] * (girl_first[1] - self.expected_value(girls_score[0], girls_score[1])),
                      girls_score[1] + koefficients[1] * (girl_second[1] - self.expected_value(girls_score[1], girls_score[0])))
        # Save rating for first girl
        for rating, girl in zip(new_rating, (girl_first, girl_second)):
            self.cursor.execute('''UPDATE girls SET rating=? WHERE filename=? ''', (rating, girl[0]))


    def get_top(self):
        return self.cursor.execute('''SELECT * FROM girls ORDER BY rating DESC LIMIT 100''').fetchall()