from app import __version__
import pytest

from calculations import add, BankAccount, InsufficientFunds


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def zero_bank_account():
    return BankAccount(starting_balance=0)


@pytest.fixture
def bank_account():
    return BankAccount(starting_balance=50)


@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (7, 1, 8), (12, 4, 16)])
def test_add(num1, num2, expected):
    print("Testing function")
    assert add(num1, num2) == expected


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize(
    "deposited, withdrawn, final_balance",
    [(200, 100, 100), (170, 50, 120), (300, 290, 10)],
)
def test_bank_transaction(zero_bank_account, deposited, withdrawn, final_balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == final_balance


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
