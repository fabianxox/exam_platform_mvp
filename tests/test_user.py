import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

import uuid

client = TestClient(app)

def test_create_user():

    email = f"test_{uuid.uuid4()}@example.com"

    response = client.post(
        "/user",
        json={
            "email": email,
            "password": "123456"
        }
    )

    assert response.status_code == 201

def test_duplicate_create_user():

    email = f"test_{uuid.uuid4()}@example.com"

    response = client.post(
        "/user",
        json={
            "email": email,
            "password": "123456"
        }
    )

    response = client.post(
        "/user",
        json={
            "email": email,
            "password": "123456"
        }
    )


    assert response.status_code == 409

def test_invalid_user():

    email = f"test_{uuid.uuid4()}@example.com"

    response = client.post(
        "/user",
        json={
            "email": email,
            "key": "123456"
        }
    )

    assert response.status_code == 422

from core.hash import hash_pw
def test_pw_hash():
    password= "password"
    has= hash_pw(password)

    assert password!=has