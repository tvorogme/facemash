#!/usr/bin/env python
# coding=utf-8
import sqlite3
from os import listdir
from os.path import isfile, join



class DataUtils:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        files = [f for f in listdir('data') if isfile(join('data', f))]

        try:
            print('Create table.')
            self.cursor.execute('''CREATE TABLE gifs (filename text, rating INT)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass
        update_girs(self)

    def update_girs(self):
        filenames_in_data = self.cursor.execute('SELECT filename FROM gifs').fetchall()

        for filename in files:
            if (filename,) not in filenames_in_data:
                self.cursor.execute('''INSERT INTO gifs VALUES ('{0}', 0)'''.format(filename))

        self.conn.commit()
