import sys

app = None

cache_file = sys.path[0] + "\\cache\\cache.json"
cache = {}

db = sys.path[0] + "\\cache\\main.db"

session = False
user_id = None
expiration_date = None
user_key = None
