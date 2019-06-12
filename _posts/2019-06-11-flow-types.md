---
title: Flow Intersection Type
categories:
- programming
tags:
- javascript
- typing
---

While working on some React components, I ran into some flow issues.
They hurt my head to understand and I'm hoping that by writing some of this down, I can better understand it.

# Flow Type Inference

Flow has powerful type inference.
This means that you only need to specify the types at the source.
Flow is able to know all the objects, trace the calls, etc. and know that `foo` is of type `TypeA`, which has a set of
fixed properties.
It knows this, even though you didn't specify the type for the function call.

I don't truly understand this but from first-hand experience, I can say that it's really, really smart.
And accurate.
The downside of this powerful inference is that when it fails, the errors are incredibly cryptic and plentiful.
The amount of errors is understandable, when you're wrong the type errors will propagate and Flow won't have the
information to infer.
No information to infer and incorrect typing look the same to Flow.
The cryptic error can be avoided by "setting up boundaries", instead of solely relying on inference.
This means explicitly declaring the type you expect, then the errors will only propagate until it reaches the
incompatible interface.

# Exact

In Javascript, everything is an object.
They're not like instances of a class, like in many languages.
After constructing an object, it's still possible to extend it with more attributes.

Flow has [`Exact`][3] types that will prevent this.
This is useful for catching typos, because the misspelled property won't match expected type.

[3]: https://flow.org/en/docs/types/objects/#exact-object-types-

# Union Type

It's somewhat common to expect two same-ish objects.
Maybe you have a `Teacher` and a `Student`, who are both `Person`.
Maybe the `Student` has id that is type `StudentId`, while the `Teacher` has id that is of type `TeacherId`.
You can use [`Union`][1] to declare that a variable is of either type.

```js
type Person =
    | Teacher
    | Student

function(user: Person){
}
```

In many OOP languages, this would be handled via inheritance and overridden functions.
But in javascript, you can use `typeof` to check the type and change the code flow.
And Flow is smart enough to recognize `typeof` checks, such that the variable is resolved to one type for that code block!

[1]: https://flow.org/en/docs/types/unions/

# Intersection Type

[`Intersection`][2] types are used to extend type objects.
This is very common.

A `Person` has `age` and `name`, while a `Student` will have an additional `studentId`.

```js
type Person = {
    age: int,
    name: string,
}

type Student =
    & Person
    & {
        studentId: int,
    }
```

This let's you DRY up types.

[2]: https://flow.org/en/docs/types/intersections/

## Caveat

You cannot have an [intersection of exact props][4].
Folks smarter than I have commented on this.
I don't really understand why I can't have `A` Or `B`, where `A` has a specific set of attributes and `B` has another
specific set of attributes.

[4]: https://github.com/facebook/flow/issues/4946

You need to make then inexact types and then you can intersect them.
The trade-off is the type checking for extraneous properties, once you resolve the types.

The workaround is to not use these fancy Flow Intersection types.
Instead, use ES6 spread operator.

```js
type Person = {|
    age: int,
    name: string,
|}

type Student = {|
    ...Person,
    studentId: int,
|}
```

Conceptually, it's the same intent the developer desired.
i.e. "Include the properties from that other type into this new type".
But it allows for use of exact types, which is quite beneficial.
This feels like a technical or philosophical limitation, on Flow's part.
