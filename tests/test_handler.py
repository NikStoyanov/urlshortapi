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


def test_encode(client):
    response = client.post('encode/test')
    assert response.status_code == 200


def test_decode(client):
    response = client.get('/6yXPbV3')
    assert response.status_code == 302
