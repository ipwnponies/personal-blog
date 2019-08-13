---
title: Shallow Vs. Mount
categories:
- programming
tags:
- react
- testing
---

Enzyme is a library for testing react components.
It handles the mounting and manipulating components.

There are 3 ways to mount a component:

- shallow
- mount (full DOM rendering)
- render

Each is used for different purposes but I found the docs and existing code base to be very confusing to understand.
Thankfully, I found a [github comment][1] that answers exactly that question.

[1]: https://github.com/airbnb/enzyme/issues/465#issuecomment-227697726

# Shallow

Shallow rendering will not render the child components.
This is useful because it sets an effective boundary.
It feels like writing a python unit test and mocking functions that are called.

```jsx
const component = shallow(<Foo>
    <Button/>
</Foo>
);
```

In this example, the mounted component will have a `<Button>` component, which is not expanded to what it actually is,
an html `<button />`.

# Mount

Mount (also known as full DOM rendering) will recursively render the children.
This makes it heavier but you end up with something more representative of a real output.

```jsx
const Button = <button href='sfdsf'/>

const component = mount(<Foo>
    <Button/>
</Foo>
);
```

When this is mounted, `<Button>` is expanded to show that it's composed of an html `<button />`.
As you can imagine, the deeper and more complex your components, the larger the expanded output.

# Render

This will render the component but not mount it.
That is, no life-cycle events are invoked.
This can be useful for verifying static components and asserting their html representation.

# Life Cycle

React components are dynamic.
You can have logic that fires during start up, change, tear down, etc.
This is what's referred to as life cycle events.

Both `shallow` and `mount` invoke life cycle events, while `render` does not.

# Summary

And here we are, with the conclusion and summarization of what to use and where.

Use `shallow` when possible: it's lightweight, maintains separation of concerns for testability, and has life cycle events.
Really prefer this for unit tests, it's minimizes the mocking boilerplate by design and lets you really focus on the
feature under test.

Use `mount` if you want to test the component, as it would be rendered at runtime. This can be thought of as useful for
"integration" testing.

Use `render` if you're interested in the html output.
Not quite sure why you couldn't use `html()`.
Avoid this, as it begins to stray too far away from testing within React's domain.
