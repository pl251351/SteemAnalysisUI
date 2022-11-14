from os import environ as env

API_KEY = env['WATSON_API_KEY'] if 'WATSON_API_KEY' in env else print(
    "No WATSON_API_KEY is set - "
    "this will fail")

URL = env['WATSON_URL'] if 'WATSON_URL' in env else print(
    "No WATSON_URL is set - "
    "this will fail")
DATA_DIR_PREFIX = "Something"
