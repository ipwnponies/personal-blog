---
title: React Ref Forwarding
categories:
- programming
tags:
- react
---

I needed to implement impression logging on a React component and wanted to use the [intersection-observer package][1].
This is react library to interface with the _[Intersection Observer API][2]_ and trigger events when html elements come
into the viewport.

[1]: https://www.npmjs.com/package/intersection-observer
[2]: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API

React components exist in the virtual DOM but the Web API is implemented for physical DOM objects.
The virtual dom is an abstraction layer but sometimes you need reference to the underlying html elements, so that you
can use the web api directly, instead or relying on React bindings to proxy it forward.

This is done by [forwarding a reference][3].
This reference object is shuttled down the component tree until it is attached to the html element.
Now the reference can be used as a worm tunnel to directly access the element, and you can perform actions directly or
change the node as you see fit.

[3]: https://reactjs.org/docs/forwarding-refs.html
