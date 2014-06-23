from flask import current_app

from . import api1_0

@api1_0.route('/', methods=['GET'])
def main():
    return "OK"



