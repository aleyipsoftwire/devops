## The Brief

This exercise teaches the skills to implement unit and integration tests in a Python & Flask codebase, as well as add new features following the Test Driven Development (TDD) methodology. We'll be working on an existing codebase for a (very simple!) JSON banking API. Alongside testing, you'll gain hands-on experience expanding a web API using Python. 

We'll also take the opportunity to show some new Python concepts and libraries that will help further develop the programming skills developed earlier in this course.

## Setup

Clone this repository onto your computer.

Follow the README instructions to launch the app and run the tests.

Before starting, take some time to explore the app and codebase – but don’t worry about understanding everything. The key thing to understand for the first exercise is the code you will be testing, which is all in bank.py.

> [Type Annotations](https://docs.python.org/3/library/typing.html): These are optional in Python, but help document your code and allows your editor provide more informative prompts. They are not actually enforced when running the code

## Codebase Tour – Tests

This exercise is about testing, and we've given you a head start! Run `poetry run pytest` from the root of the repository. Pytest will detect the test files already present, and should give output that looks that shown below. Through this exercise you'll add more tests to this suite.

```
$ poetry run pytest
> ================== test session starts ================== 
> platform darwin -- Python 3.8.1, pytest-5.4.2, py-1.8.1, pluggy-0.13.1
> rootdir: /Users/robowe/Academy/DevOps-Course-TDD
> collected 5 items
> 
> tests/test_app.py .                              [ 16%]
> tests/test_bank.py ....                          [100%]
> 
> ================== 5 passed in 0.26s ==================
```

Try reading the tests in /tests/test_bank.py and understand how they work. Each function beginning with "test_" is a test. When a test has a parameter (like these all have a parameter called `bank`), then pytest will provide a value for it. In this case, there is a pytest "fixture" defined at the top of the file, also called `bank`. Because the two names match, pytest runs that fixture function before each test to provide each test with its own independent, empty instance of `Bank`.

## Part 1 - Unit Tests

Look at the tests in `/tests/test_bank.py`. They do a good job of covering the account creation aspects of the bank class, but it appears the previous developer forgot to test the `add_funds()` method on the `Bank` class. You should:

1. Add unit tests for `add_funds()`
1. Run them with `pytest`
1. Review any failures. Is the test flawed, or have you discovered a bug?
1. Fix any bugs identified

**Hints:**
- Try to think of edge cases – can you come up with at least 3 useful test cases? If the `bank.py` code does not handle the edge cases how you would like, then you are welcome to modify it.
- Make sure pytest detects and runs your tests! If it doesn’t, make sure your files and test functions are named correctly.

## Codebase Tour - app.py and flask-restx

The `app.py` file configures Flask and defines the API endpoints. For this exercise we’re using a second library, `flask-restx`, to enhance flask with functionality that's helpful for writing a REST JSON API. This includes automatically returning responses as JSON, and other bells and whistles like the Swagger documentation already seen.

You don't need to learn the details of `flask-restx` (see the [docs](https://flask-restx.readthedocs.io/en/latest/) if you're interested), but it's useful to recap how the routes are structured as it's a bit different to vanilla flask. This may look a little odd, but give it a try and you'll find it's a very sensible way of doing things for a REST API! The Products class could be expanded with other methods (e.g. `post()`, `patch()`, `put()`, `delete()`) to handle additional HTTP methods.

## Part 2 - Integration Tests

You now have a complete unit test suite for the Bank class, but what about all that complicated stuff in `app.py`? This code is an interface between two components of the system: application logic and API framework, and this makes it a poor candidate for unit testing. Remember, unit tests don't run across interfaces – that's a job for integration tests.

Unfortunately, the previous developer didn't care much for integration tests. You'll need to write them. You don't need loads of integration tests, perhaps just one or two in this case. Integration tests check that the components of the system work together correctly. They don't need to handle every single edge case - that's a job for unit testing.

Write an integration test in `test_app.py` that uses the client fixture to send a request to the `Accounts` resource POST endpoint (i.e. a POST request to `/accounts/<account name here>`). Check the response status code and body to ensure the item was created correctly. Instead of trying to understand the `app.py` file you should be able to find everything you need to know from the interactive Swagger site. 

Expand your integration test to also check you can query the created account via the `Accounts` resource GET endpoint (i.e. a GET request to the same path)

<details markdown="1"><summary>Hint for making assertions about the response</summary>

The result of `client.get` or `client.post` is a test response object, containing all the things you would expect from an HTTP response. Two attributes you probably want to look at are:
- `status_code` - a number, e.g. 200 for a status of "OK".
- `data` - the response body. This is a byte array rather than a string, because not all HTTP bodies just hold text. So you have to either compare it to another byte array in your assertion, or convert it to a string first: `response.data.decode()`

</details>

## Stretch Goals

### New feature with TDD and mocking

We'd like to add functionality to query an account's current balance. The bank doesn't store balances – it stores a set of transactions – but a balance could be calculated by summing all the transactions on an account. This kind of analytics / reporting behaviour doesn't belong on the Bank class itself (remember separation of concerns), so we should create a new class. Let's call it `BankReport`. This is a class that can generate extra useful metrics and analyses from a Bank instance.

To demonstrate, we want to be able to use a `BankReport` class like this:

```python
bank = Bank()
bank_report = BankReport(bank)
bank.create_account('demo')
balance = bank_report.get_balance('demo') # expect balance == 0
```

1. Create a new file (bank_report.py) to store the new class.
1. Build the `BankReport` class strictly following test-driven development (TDD):
    * Write a unit test
    * Write the mimimal application code that makes the test pass
    * Refactor
    * Repeat
1. Modify app.py to expose a GET endpoint where clients can query an account's balance.
    * This could be a new endpoint, or perhaps added to the response from GET /account/<name>
1. Write integration tests to check your endpoint works, and correctly displays any funds added.

Once complete, review your unit tests. How do they look? Something like below?

```python
def test_bank_report():
    bank = Bank()
    bank_report = BankReport(bank)
    # Set up some accounts...
    # Add some money...
    # Call methods on bank_report...
    # Check balance matches input money...
```
This test will work, but it isn’t a strict unit test. By using functionality from the `Bank` class, our test is implicitly testing that as well. 

We need to mock the `Bank` class. Python has several options for doing so, here we'll use pytest's built-in `monkeypatch` fixture. The code below demonstrates how to use this.

```python
def test_bank_report(monkeypatch):
    bank = Bank()
     
    def mock_acc(name):
        return Account(name)
 
    monkeypatch.setattr(bank, 'get_account', mock_acc)
    # bank.get_account(name) is now mocked
    # Test continues...
```

1. Re-write your `BankReport` unit tests to mock the relevant Bank methods and attributes.
    * This will need to include `get_account` and `transactions`
1. Make a temporary edit to your code that breaks the `Bank` class. Re-run your unit tests to check that the `Bank` unit tests fail and the BankReport unit tests pass.

### Move money between accounts

At the moment, the banking API only supports external deposits. It really should support moving money between two accounts within the bank. Deliver this feature using strict test-driven-development, similar to Part 3. The end result should be:

* A new API endpoint at `/money/move` (POST)
* A move_funds method on the `Bank` class
* Unit tests for the `move_funds` method (including error handling)
* Integration tests for moving money between accounts

> Note: A fund transfer should be recorded as a pair of transactions, one on each account, with identical timestamps and opposite values (i.e. one will be negative). Your tests should ensure that money is travelling the right way, and that the total amount on money in the bank doesn't change.

### Disallow overdrafts

Your bank currently allows users to withdraw or send money even if they are overdrawn (i.e. their balance is less than zero). Following TDD, add unit tests and integration tests to check that moving money from an overdrawn account fails, and that the client is returned an appropriate HTTP error code if they try to take an account overdrawn. Add functionality to satisfy your tests. Make sure you pay attention to the 'Refactor' step in the Red-Green-Refactor cycle!

### Add type checking

Download and run mypy against your code. mypy is a Python static analysis tool that checks your type annotations for potential errors. Does it find any issues? If you haven't done so already, try adding type hints to all your code and validate them using mypy.

### (Hard!) Add data persistence

The bank currently stores everything in memory only - that's not great! What if the server needs to restart? Refactor the `Bank` class to use sqlite3 database instead of the `accounts` and `transactions` collections to store its data. Add unit tests for any new classes created. We don't advise picking up this task unless you're already familiar with SQL databases.
