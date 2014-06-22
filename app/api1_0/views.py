from flask import current_app

from . import api1_0

@api1_0.route('/')
def main():
    return "OK"
