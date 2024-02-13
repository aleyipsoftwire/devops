"""Unit tests for bank.py"""

import pytest

from bank_api.bank import Bank


@pytest.fixture
def bank() -> Bank:
    return Bank()

def test_create_account_raises_error_if_name_blank(bank: Bank):
    # This means: assert an exception is raised during the following block
    with pytest.raises(Exception):
        bank.create_account('')

def test_create_account_raises_error_if_name_contains_only_space(bank: Bank):
    # This means: assert an exception is raised during the following block
    with pytest.raises(Exception):
        bank.create_account(' ')

def test_bank_creates_empty(bank: Bank):
    assert len(bank.accounts) == 0
    assert len(bank.transactions) == 0

def test_can_create_and_get_account(bank: Bank):
    bank.create_account('Test')
    account = bank.get_account('Test')

    assert len(bank.accounts) == 1
    assert account.name == 'Test'

def test_get_account_raises_error_if_no_account_matches(bank: Bank):
    bank.create_account('Name 1')

    # This means: assert an exception is raised during the following block
    with pytest.raises(ValueError):
        bank.get_account('Name 2')

@pytest.mark.parametrize("amount", [10, -10])
def test_can_add_funds(bank: Bank, amount: int):
    account_name = 'Name 1'
    bank.create_account(account_name)

    bank.add_funds(account_name, amount)

    assert bank.transactions[-1].account.name == account_name
    assert bank.transactions[-1].amount == amount

def test_can_add_empty_funds(bank: Bank):
    account_name = 'Name 1'
    amount = 0
    bank.create_account(account_name)

    with pytest.raises(ValueError):
        bank.add_funds(account_name, amount)

def test_add_funds_raises_error_if_no_account_matches(bank: Bank):
    with pytest.raises(ValueError):
        bank.add_funds('Name 1', 0)
