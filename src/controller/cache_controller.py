import os
import sys
import json
from datetime import date, datetime
from src.controller import config
from src.view import *

def init_cache():
    try:
        db = ((str(open(config.db, "x"))).split("'"))[1]
        print("db created")
    except FileNotFoundError:
        os.mkdir(sys.path[0] + "\\cache")
        db = ((str(open(config.db, "x"))).split("'"))[1]
        print("cache folder and db created")
    except FileExistsError:
        print("db already exists")

    try:
        open(config.cache_file, "x")
        cache = {
            "SESSION": {},
            "DB": config.db
        }

        with open(config.cache_file, "w") as cache_file:
            json.dump(cache, cache_file, indent=4)

        print("cache file created")
    except FileExistsError:
        with open(config.cache_file, "r") as cache_file:
            update_cache(json.load(cache_file))

        print("cache file already exists")

    print(check_session())

def update_cache(cache: dict):
    # cache:
    #     {
    #         "SESSION": {
    #                 "ID": id,
    #                 "EXPIRATION_DATE": expiration_date,
    #                 "KEY": key
    #             },
    #         "DB": db
    #     }

    with open(config.cache_file, "w") as cache_file:
        json.dump(cache, cache_file, indent=4)

    config.cache = cache

    config.session = True if cache['SESSION'] else False

    if config.session:
        config.user_id = cache['SESSION']['USER_ID']
        config.expiration_date = cache['SESSION']['EXPIRATION_DATE']
        config.user_key = cache['SESSION']['USER_KEY']

def check_session():
    if config.session:
        if date.today() < datetime.strptime(config.expiration_date, "%Y-%m-%d").date():
            vault.manager()
            return "connected!"
        else:
            config.cache['SESSION'] = {}
            update_cache(config.cache)
            login_view.login_page()
            return "session expired!"
    else:
        login_view.login_page()
        return "no session"



