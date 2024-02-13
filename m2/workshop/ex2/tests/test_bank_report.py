"""Unit tests for bank_report.py"""

import pytest

from bank_api.bank import Bank
from bank_api.bank_report import BankReport


@pytest.fixture
def bank() -> Bank:
    return Bank()

@pytest.fixture
def bank_report(bank: Bank) -> BankReport:
    return BankReport(bank)

def test_returns_0_for_empty_acount(bank: Bank, bank_report: BankReport):
    # Given
    account_name = 'account name'
    bank.create_account(account_name)

    # When + Then
    assert bank_report.get_balance(account_name) == 0

def test_returns_account_balance(bank:Bank, bank_report: BankReport):
    # Given
    account_name = 'account name'
    amount = 10
    bank.create_account(account_name)
    bank.add_funds(account_name, amount)

    # When + Then
    assert bank_report.get_balance(account_name) == 10

def test_returns_account_balance_when_multiple_transactions(bank:Bank, bank_report: BankReport):
    # Given
    account_name = 'account name'
    bank.create_account(account_name)
    
    amount_1 = 10
    bank.add_funds(account_name, amount_1)
    
    amount_2 = -20
    bank.add_funds(account_name, amount_2)

    # When + Then
    assert bank_report.get_balance(account_name) == amount_1 + amount_2
