"""Integration tests for app.py"""
from typing import Type
from flask.testing import FlaskClient
from flask.wrappers import Response
import pytest

from bank_api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_account_creation(client: FlaskClient):
    # Given
    account_name = 'example_account_name'

    # When
    response = client.post(f'/accounts/{account_name}')

    # Then
    assert response.status_code == 200
    assert response.data.decode() == f'{{"name": "{account_name}"}}\n'

def test_account_creation_with_empty_name(client: FlaskClient):
    # Given
    account_name = ' '

    # When
    response = client.post(f'/accounts/{account_name}')

    # Then
    assert response.status_code == 400
    assert response.data.decode() == '{"message": "Account name cannot be None or empty"}\n'

def test_account_fetching(client: FlaskClient):
    # Given
    account_name = 'example_account_name'
    client.post(f'/accounts/{account_name}')

    # When
    response = client.get(f'/accounts/{account_name}')

    # Then
    assert response.status_code == 200
    assert response.data.decode() == f'{{"name": "{account_name}"}}\n'

def test_returns_404_when_account_not_found(client: FlaskClient):
    # Given
    account_name = 'example_account_name'

    # When
    response = client.get(f'/accounts/{account_name}')

    # Then
    assert response.status_code == 404
    assert response.data.decode() == '{"message": "Account not found"}\n'

def test_get_account_balanace(client: FlaskClient):
    # Given
    account_name = 'example_account_name'
    client.post(f'/accounts/{account_name}')

    # When
    response = client.get(f'/balance/{account_name}')

    # Then
    assert response.status_code == 200
    assert response.data.decode() == '{"balance": 0}\n'

def test_get_account_balance_returns_404_when_account_not_found(client: FlaskClient):
    # Given
    account_name = 'example_account_name'

    # When
    response = client.get(f'/balance/{account_name}')

    # Then
    assert response.status_code == 404
    assert response.data.decode() == '{"message": "Account not found"}\n'

def test_get_account_balance_returns_correct_amount_after_adding_funds(client: FlaskClient):
    # Given
    account_name = 'example_account_name'
    client.post(f'/accounts/{account_name}')

    client.post(f'/money', json={
        'name': account_name,
        'amount': 10
    })

    client.post(f'/money', json={
        'name': account_name,
        'amount': -5
    })

    # When
    response = client.get(f'/balance/{account_name}')

    # Then
    assert response.status_code == 200
    assert response.data.decode() == '{"balance": 5}\n'
