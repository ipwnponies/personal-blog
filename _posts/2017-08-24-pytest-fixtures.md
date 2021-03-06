---
title: Pytest Fixtures
---
# pytest fixtures
## Documentation
Official docs are at https://docs.pytest.org/en/latest/fixture.html

## What are fixtures?
In the unit testing world, fixtures are code components that create and set up the environment before tests are run. 
Fixtures are commonly used for:
* Loading initializing test data
* Monkey patching out calls to the real world with calls to mocks instead
* Getting the system into a state we want to test
  * Get test user into logged in state, with existing session
  * Trigger loading of configs
  
It's important to be able to reliably reproduce the environment; nobody likes flakey tests!
The unit testing framework will allow for syntactic sugar to make it easier on the eyes when coding.
pytest does this by auto-loading fixtures that are specified in parameter when running test cases.

## How to do this with pytest
```python
import pytest

@pytest.fixture
def some_specific_test_setup():
  # Setup stuff
  db = {
    'key1': 'value1',
    'key2': 'value2',
  }
  
  # Return execution to the unit test
  yield db
  
  # Fixture cleanup
  teardown_and_cleanup(db)


def test_unittest(some_specific_test_setup):
  assert 'key1' in db
```
The `pytest.fixture` decorator is used to denote a function that will serve as the fixture call.

With the use of the `yield` keyword, execution is given back to the unit test.
When the test completes, execution returns back to fixture and custom teardown logic can be done.

## Scope
Fixtures can execute for each test case ('function'), each module ('module'), or once for entire test run ('session').
This is controlled with the `scope` parameter:
```python
pytest.fixture(scope='session')
```
The default is 'function', which means fixture setup and teardown is done for each test, isolating them.
This is highly preferred but if the setup/teardown is expensive, shared use of a fixture can be employed.
Be careful to ensure that this does not introduce dependency on ordering of test execution due to test pollution.

## autouse
If a fixture is to be used for all test cases, use the `autouse` parameter:
```python
pytest.fixture(autouse=True)
```
This will implicitly run it for all tests. This can be useful for:
* setting up a common initial set of test data
* mocking out a service call in all places (there are other ways around this issue but that's outside the scope of this post)

## conftest.py
The `conftest.py` is implicitly imported into every test module in the same directory. Put fixtures that are intended to be shared across modules in here.

## Parametrizing Fixtures
Fixtures can be parametrized using the `params` parameter:
```python
@pytest.fixture(
  params=[
    'alice',
    'bob',
  ],
)
def setup_user(users):
    return db.get_session(users.param)
```
This fixture will run the test case with the `alice` user session setup first, then it will run again for `bob`.
This feature can be handy for running tests:
* against multiple db orms
* testing different users acls

This is similar to parametrizing unit tests but this will re-run all the tests universally.
This feature is more suited when you have different actors on your systems and you expect to run all the tests for each actor.
