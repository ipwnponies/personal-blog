---
title: Saving Requests Data for Testing
categories:
- programming
tags:
- python
- testing
- ipython
---

I wanted to contribute to [mealpy](https://github.com/edmundmok/mealpy) and had grand ideas.
But the timing was unfortunate, as I only had 2 more days left on my meal plan until I put it on hold.

How do I test if the endpoints no longer work for an "unauthenticated" user?
My strategy was to serialize the response from the endpoints and store them for processing.
I plan to rip out sensitive information and eventually use them as the basis for a mock responses in the unit tests.

# Saving Requests Data

For testing, I wanted to mock out the responses to certain API to simulate the test case.
I don't actually want to login with real credentials and I don't want to purposefully fail login continuously.

What I wanted to do was some Test Driven Development.
And I needed to be able to mock the responses.

I use [PUDB](https://github.com/inducer/pudb) as my python debugger of choice.
Put a breakpoint right after making `requests` call and the run the script.
You'll be dropped into a debugging environment at the right spot to capture the response.
Switch to ipython (using `!` shortcut).
From here, we have the response object and our goal is to serialize it for persistence.

## ipython

You could use [`ipython` `storemagic`] to achieve this.
Note, for some reason you need to load the extension manually when invoked through `pudb`, when it's automatically
loaded when running `ipython` directly.

[`ipython` `storemagic`]: https://ipython.readthedocs.io/en/stable/config/extensions/storemagic.html

```python
%store response
```

This will save the object in python.
At a later time, you can load the object back for inspection:

```python
%store -r response
```

Don't bother using the "store to file" option, there's no option to reload objects back from file.

## Pickling

Since I want to use this response for tests, I didn't want to use `storemagic`, since it requires `ipython` to read back.
Instead, we fallback to using common serialization methods: `json`, `pickle`, `yaml`, etc.

I chose `pickle` since I was in a rush and it just works™.
What `pickle` does is store all the metadata information inside the object and `eval` it back into existence.
Note, this form of de-serialization can be dangerous because code is actually executed.
In my case, it was fine because I created the object, using common library `Requests`.
The same issue exists in `PyYaml`, when not using `safe_load`.

```python
In [1]: import pickle; pickle.dump(response, open('get_current_meal.txt', 'wb'))
In [2]: response = pickle.load(open('get_current_meal.txt', 'rb'))
```

I repeated this for every request call, for every edge case, saving each response to a separate, well-named text file.
Now I have all the data I need to write some tests!
