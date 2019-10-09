"""
URL shortening API in AWS lambda and DynamoDB.
"""

import os
import uuid
import json
import boto3
from flask import Response

from urlshortapi import app

ALPHABET = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
BASE = len(ALPHABET)


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


def build_dbconn(linkstable='UrlShortener'):
    """
    Builds the connection string to the database.
    """

    if 'TESTING' in os.environ:
        profile_name = 'zappa-deploy'
        linksregion = 'eu-west-2'
        session = boto3.Session(profile_name=profile_name)
        dynamodb = session.resource('dynamodb', region_name=linksregion)
    else:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(linkstable)

    return table


@app.route('/encode/<path:url_string>', methods=["POST", "GET"])
def encode(url_string):
    """
    Encode uuid for a given input URL.
    """

    id_num = gen_id()
    db_uuid = id_num
    encoded_uuid = ''

    while id_num > 0:
        encoded_uuid = ALPHABET[id_num % BASE] + encoded_uuid
        id_num //= BASE

    # Insert new entry in dynamodb
    table = build_dbconn()
    response = table.put_item(
        Item={
            'url_string': url_string,
            'uuid': str(db_uuid)
        }
    )

    # Return encoded url string
    response_msg = '{"encoded_uuid": "' + encoded_uuid + '"}'
    response = json_response(json.loads(response_msg), status=json.dumps(
        response['ResponseMetadata']['HTTPStatusCode']))
    return response


@app.route("/decode/<string:encoded_uuid>", methods=["POST", "GET"])
def decode(encoded_uuid):
    """
    Decode a string to uuid.
    """

    db_uuid = 0

    for char in encoded_uuid:
        db_uuid = db_uuid * BASE + ALPHABET.index(char)

    # Read entry in dynamodb
    table = build_dbconn()
    response = table.get_item(
        Key={
            'uuid': str(db_uuid)
        }
    )

    # Return url from encoded url string
    response_msg = '{"url_string": ' + json.dumps(
        response['Item']['url_string']) + '}'
    response = json_response(json.loads(response_msg), status=json.dumps(
        response['ResponseMetadata']['HTTPStatusCode']))
    return response
