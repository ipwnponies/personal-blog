---
title: Generics with Flow
categories:
- programming
tags:
- javascript
- type system
---

Generics are a type system concept that allows for dynamic typing, as opposed to static typing.

## Primer

### Static Typing

[Static typing][1] is what we are most familiar with and the most straight forward.

[1]: https://flow.org/en/docs/types/primitives/

```js
// @flow
const count: number = 2;
```

### Inference

Flow is powerful enough to infer types and doesn't require us to statically declare every variable's type.
This is extremely convenient and many modern languages incorporate some inference to reduce the boilerplate and overhead.

```js
// Automatically infer type, by drilling down all the way to a concrete declaration
const count = 3;
const countFromMethod = getNumberFromDb();
```

But don't abuse this, that's a rookie mistake.
Use inference for convenience but declare interface boundaries to set expectations.
This sets error boundaries and limits the scope of type checking bugs.

```js
// Don't infer type, set an interface boundary
const count: number = get_number_str(); // error
console.log(count.toFixed()) // No type error but still going to blow up at runtime

const rookieMistakeNum = incorrect_function_returning_string(); // wrong type silently returned
return rookieMistakeNum.toFixed() // Misleading flow error
```

**Protip:** Definitely always statically declare types of encapsulated objects.
If I'm using your library and your doc says it takes a boolean, I don't care about bugs in your code where you return a
string instead.
That's on you, don't cause noise on my end.
Declare your types so that I don't have errors, your code will correctly error out during development, and you catch this
before releasing to the world.

## Generics

On to generics, definitely read up on [wikipedia][2].
[Flow generic reference][3]

[2]: https://en.wikipedia.org/wiki/Generic_programming
[3]: https://flow.org/en/docs/types/generics/

### Simple Example

A simple and contrived/useless example is a function that accepts a type and returns the same type:

```js
// Generic. T is a type "variable", everywhere you see T, replace it with a concrete type
const returnSameThing<T> = (foo: T) => foo;

// Number
const returnSameThingNum = num: number => num;
const number = 2;
// Literally resolves to the same thing
returnSameThingNum(number);
returnSameThing(number));

// String
const returnSameThingStr = string: string => string;
const string = 'blah';

returnSameThingStr(string);
returnSameThing(string);
```

We can already see how expressive generics can be, as single generic will handle unlimited types.
It's parameterizing but at a type system level.

Let's think of a less useless example:

```js
const animalReproduce<T> = (parent: T) => {
  const offspring = parent.reproduce(); // Offspring is of same type as parent
  console.assert(offspring.parent === parent);
  return offspring
}

const bear = new Bear();
const deer = new Deer();

const babyBear: Bear = animalReproduce(bear);
const babyDeer: Deer = animalReproduce(deer);
const babyBearFromDeer: Bear  = animalReproduce(deer); // Error, type returned will always be Deer
```

In this example, we are able to "reuse" `animalReproduce` for produce new objects that are typed.
This is not inference, we have leveraged generics to enforce type strict constraints:
a bear will only ever produce a bear and a deer will only ever produce a deer.
This is not a coincidence or clever programming, this is literally the textbook use case for generics.

### React and Redux

In React, the use of generics will likely arise due to dependency injecting values to a component from redux store.
i.e. We want a convenience wrapper that is capable of automatically grabbing a value form redux context and inserting it
to a wrapped component.
In practice, this means our `BaseComponent` has **N** props while our output `ReduxWrappedComponent` will have **N-M** props,
for **M** injected props.

```js
type InjectedProps = {
  foo: boolean,
  bar: number,
}
const withFooAndBarInjected<T: {InjectedProps}> = (
  component: ComponentType<T>
): ComponentType<$Diff<T, InjectedProps>> => {
  return connect(mapStateToProps)(component)
}

// Component requires all these values and is agnostic to where it's from
const InternalComponent = ({foo, bar, baz}) => {
  return <Div>{foo}{bar}{baz}</Div>
}

// Externally exposed component, conveniently with no presence of foo and bar
const Component =  withFooAndBarInjected(InternalComponent);
// <Component baz={blah} />
```

An example here is that we have values `foo` and `bar` that we want to pull and automatically injected as props.

We definitely need to use generics because we do not have all the time and energy in the world to create a bunch of `withFooAndBarInjected`
for each and every component we want to hook up.
We want `withFooAndBarInjected` to be able to automatically adapt and output a wrapped component that is still type correct.
THe magic is with [`Diff`][4], which is a set difference between the full set of props from `InternalComponent` and `InjectedProps`.
The resultant prop is dynamically calculated by flow to be only the prop we require from end user.

[4]: https://flow.org/en/docs/types/utilities/#toc-diff
