---
title: Mocking Module-level Functions in Jest
categories:
- programming
tags:
- testing
- javascript
- jest
- mocking
---

In `python`, it's pretty straightforward to mock a module level function.

```python
# File module_A.py
def function_A:
    ...

# File module_B.py
import module_A
from module_A import function_A

# Test file
import module_B

# Mock module import
with mock.patch.object(module_B.module_A, 'function_A'):
    ...
with mock.patch('module_A.function_A'):
    ...

# Mock "from-import" by targeting module_B because it holds it's own reference
# It is a pointer, we are not mocking the dereferenced object, we're changing the pointer reference to a new object altogether
with mock.patch.object(module_B, 'function_A'):
    ...
```

But in `javascript`, with `jest`, it's a bit more complex and awkward to mock module-level functions.
`jest` can only mock objects (I guess it's the same as python), so you need to get a [reference to the module][1]:

```js
const moduleUnderTest = await import('./moduleUnderTest.js');
jest.mock(moduleUnderTest, 'functionToMock');
```

[1]: https://github.com/facebook/jest/issues/936#issuecomment-214939935
