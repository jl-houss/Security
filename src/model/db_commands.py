import sqlite3
from src.controller import config

def db_connect():
    conn = sqlite3.connect(config.db)
    c = conn.cursor()
    return conn, c
