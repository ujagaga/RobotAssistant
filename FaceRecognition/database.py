#!/usr/bin/python3

import sqlite3
import os
import time


class DatabaseHandler:
    def __init__(self):
        # Initialization
        db_dir = '/tmp/.faceRecognition'
        if not os.path.isdir(db_dir):
            os.mkdir(db_dir)

        DATABASE = os.path.join(db_dir, "database.db")
        self.db = sqlite3.connect(DATABASE)

        # Initialize the table
        try:
            sql = "create table faces (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, face_at_x INTEGER, " \
                  "face_at_y INTEGER, img_w INTEGER, img_h INTEGER, conf INTEGER, time INTEGER)"
            self.db.execute(sql)
            self.db.commit()
        except Exception as e:
            print("Warning: failed to create database table: {}".format(e))

    def query_db(self, query, args=(), one=False):
        cur = self.db.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def get_face(self, name):
        sql = "SELECT * FROM vars WHERE name = '{}'".format(name)
        result = self.query_db(sql, one=True)

        return result

    def update_face(self, data):

        if 'name' in data.keys():
            sql = "SELECT id FROM faces WHERE name='{}'".format(data['name'])
            result = self.query_db(sql, one=True)

            if result is None:
                sql = "INSERT INTO faces (name, face_at_x, face_at_y, img_w, img_h, conf, time) VALUES " \
                      "('{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
                      "".format(data['name'], data.get('face_at_x', 0), data.get('face_at_y', 0), data.get('img_w', 0),
                                data.get('img_h', 0), data.get('conf', 0), int(time.time()))
            else:
                sql = "UPDATE faces SET face_at_x='{}', face_at_y='{}', img_w='{}', img_h='{}', conf='{}', time='{}'" \
                      "WHERE name='{}'".format(data.get('face_at_x', 0), data.get('face_at_y', 0), data.get('img_w', 0),
                                               data.get('img_h', 0), data.get('conf', 0), int(time.time()), data['name'])

            self.db.execute(sql)
            self.db.commit()

    def close(self):
        self.db.close()
