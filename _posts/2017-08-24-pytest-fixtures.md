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
