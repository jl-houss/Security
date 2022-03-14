from src.controller import config, cache_controller
from src.model import *
from src.view.Base import vault
from src.view.Connections import login_view
from datetime import date, timedelta
from backports.pbkdf2 import pbkdf2_hmac

import bcrypt
import binascii
import json


def login(email: str, password: str, session: bool):
    conn, c = db_commands.db_connect()
    
    c.execute("SELECT * FROM Users WHERE email=?", (email,))
    res = c.fetchone()

    if res:
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(res[2], 'utf-8')):
            print("logged")

            if session:
                expiration_date = str(date.today() + timedelta(14))
            else:
                expiration_date = str(date.today() + timedelta(1))

            salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
            key = pbkdf2_hmac("sha256", password.encode("utf8"), salt, 10000, 16)

            config.session = {
                "ID": res[0],
                "EXPIRATION_DATE": expiration_date,
                "KEY": key
            }

            cache = json.load(open(config.cache_file))

            cache['SESSION'] = {
                "USER_ID": res[0],
                "EXPIRATION_DATE": expiration_date,
                "USER_KEY": binascii.hexlify(key).decode("ascii")
            }

            cache_controller.update_cache(cache)

            vault.manager()
            return
    login_view.alert()
    