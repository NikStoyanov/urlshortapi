"""
Test the handlers.
"""

import json
import pytest

from urlshortapi import api


@pytest.fixture
def client(request):
    test_client = api.app.test_client()
    return test_client


def post_json(client, url, json_dict):
    """Helper function to send json to url."""
    return client.post(url, data=json.dumps(json_dict),
                       content_type='application/json')


def resp_json(response):
    """Helper function to decode json response."""
    return json.loads(response.data.decode('utf8'))


def test_alphabet(client):
    response = client.get('/6yXPbV3')
    assert response.status_code == 200
