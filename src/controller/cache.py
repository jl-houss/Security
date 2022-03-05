import os
import sys
import json
from datetime import date, datetime
from src.controller import config
from src.view.Connections import login

def init_cache():
    try:
        db = ((str(open(sys.path[0] + "\\cache\\main.db", "x"))).split("'"))[1]
        print("db created")
    except FileNotFoundError:
        os.mkdir(sys.path[0] + "\\cache")
        db = ((str(open(sys.path[0] + "\\cache\\main.db", "x"))).split("'"))[1]
        print("cache folder and db created")
    except FileExistsError:
        db = sys.path[0] + "\\cache\\main.db"
        print("db already exists")

    try:
        open(sys.path[0] + "\\cache\\cache.json", "x")
        cache = {
            "SESSION": {},
            "DB": db
        }

        with open(sys.path[0] + "\\cache\\cache.json", "w") as cache_file:
            json.dump(cache, cache_file, indent=4)

        print("cache file created")
    except FileExistsError:
        with open(sys.path[0] + "\\cache\\cache.json", "r") as cache_file:
            update_cache(json.load(cache_file))

        print("cache file already exists")

    print(check_session())

def update_cache(cache: dict):
    with open(sys.path[0] + "\\cache\\cache.json", "w") as cache_file:
        json.dump(cache, cache_file, indent=4)

    config.cache = cache

    config.db = cache['DB']

    config.session = True if cache['SESSION'] else False

    if config.session:
        config.user_id = cache['SESSION']['USER_ID']
        config.expiration_date = cache['SESSION']['EXPIRATION_DATE']
        config.user_key = cache['SESSION']['USER_KEY']

def check_session():
    if config.session:
        if date.today() < datetime.strptime(config.expiration_date, "%Y-%m-%d").date():
            return "connected!"
        else:
            config.cache['SESSION'] = {}
            update_cache(config.cache)
            return "session expired!"
    else:
        return "no session"



