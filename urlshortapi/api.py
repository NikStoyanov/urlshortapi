"""
URL shortening API.
"""

import uuid
import json
from flask import Response

from urlshortapi import app

ALPHABET = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
BASE = len(ALPHABET)

LINKSTABLE = "UrlShortener"
LINKSREGION = "eu-west-2"


def json_response(json_dict, status=200):
    """
    Helper for generating a json response.
    """

    response = Response(json.dumps(json_dict), status=status,
                        mimetype='application/json')
    return response


def gen_id():
    """
    Generate high probability unique ID for DynamoDB.
    """

    return uuid.uuid1().int >> 90


@app.route('/encode/<path:url_string>', methods=["POST", "GET"])
def encode(url_string):
    """
    Encode uuid for a given input URL.
    """

    id_num = gen_id()
    url_string = ''

    while id_num > 0:
        url_string = ALPHABET[id_num % BASE] + url_string
        id_num //= BASE

    response = json_response(json_dict={"url_string": url_string})

    return response


@app.route("/decode/<string:url_string>", methods=["POST", "GET"])
def decode(url_string):
    """
    Decode a string to uuid.
    """

    id_num = 0

    for char in url_string:
        id_num = id_num * BASE + ALPHABET.index(char)

    response = json_response(json_dict={"id_num": id_num})

    return response
