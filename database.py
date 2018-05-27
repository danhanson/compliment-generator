import sqlite3
import os
import uuid
import hashlib

recipients = [
    ('Chad','+16168863628')
]
users = [
    ('guest', '')
]

def connect():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.executescript('''
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS recipients (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS compliments (
    `id` TEXT PRIMARY KEY,
    `sender` TEXT NOT NULL,
    `recipient` TEXT NOT NULL,
    `content` TEXT NOT NULL,
    `date` INTEGER NOT NULL
);

''')
    for name, password in users:
        try:
            scrypt = hashlib.scrypt(bytes(password,'utf8'),salt=os.urandom(24),n=2**17,r=16,p=1,maxmem=512*1024**2)
            cursor.execute(
                'INSERT INTO users (id, name, password) VALUES (?,?,?);',
                (str(uuid.uuid4()), name, scrypt)
            )
        except sqlite3.IntegrityError:
            pass
    for name, number in recipients:
        try:
            cursor.execute(
                'INSERT INTO recipients (id, name, phone) VALUES (?,?,?);',
                (str(uuid.uuid4()), name, number)
            )
        except sqlite3.IntegrityError:
            pass
    cursor.close()
    db.commit()
    return db

