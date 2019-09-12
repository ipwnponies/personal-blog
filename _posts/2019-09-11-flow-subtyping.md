---
title: Flow Intersection Types and Casting
categories:
- programming
tags:
- flow
- javascript
- typing
---

I've talked about `Flow` types in the [past][1] but I had more recent dealings with it.
A coworker was struggling to appease the type system when trying to work in inheritance and subtyping.
The system has design issues but the scope of their changes did not warrant a large refactor.
As such, we needed to figure out the least hacky solution, given the situation at hand.

[1]: {% post_url 2019-06-11-flow-types %}

# Flow Concepts Related to Inheritance

Inheritance and Subtyping can be done with either [`Intersection`][1] or [`Union`][2].
Both come with gotchas.

[1]: https://flow.org/en/docs/types/intersections/
[2]: https://flow.org/en/docs/types/unions/

## Intersection

Intersections are an "all of" set.
This means that any the value must satisfy **all of** the types, not only one.

```js
type Text = string & localizedString;

const text: Text = 'i am a  string';
const text2: Text = i18('i am a  string');
```

It's very possible to create ["impossible" types][3]:

[3]: https://flow.org/en/docs/types/intersections/#toc-impossible-intersection-types

```js
type BooleanOrString = string & boolean;

// 'string' is not a boolean
const string: BooleanOrString = 'string';

// 123 is not a string
const number: BooleanOrString = 123;
```

These both fail horribly because no one value can satisfy both a `string` and `boolean` simultaneously.

## Union

Unions are "any of" set.
A value must satisfy **one of** the types.
This is usually what you want.

```js
type BooleanOrString = string | boolean

// Both work!
const string: BooleanOrString = 'string';
const number: BooleanOrString = 123;
```

# How to Subtype

Here is a trivial subtyping example:

```js
type Stuff = {
    name: string
};

// Using Flow intersection
type EarthStuff = Stuff & {
    fromEarth: boolean,
};

// Using js destructuring
type EarthStuff2 = {
    ...Stuff,
    fromEarth: boolean,
};
```

You can achieve subtyping with either `Flow` intersection or using javascript destructuring (`Flow` union).
These both have limitations and gotchas, so pick your poison.

## Intersection Subtyping

### Impossible Types Gotcha

When you intersect objects, the properties are merged, effectively allowing for creating a superset/subsclass.
Properties are recursively intersected.

If there are properties with the same names, then they can form impossible types.
Given that we common want to change a property to make it more specific (nullable->non-nullable) or to restrict the type
set (Base->Subclass),
this gotcha is very, very hard to avoid.

```js
type Stuff = {
    name: string,
    // This might not even apply to abstract concepts
    fromEarth: boolean | null,
};

type EarthStuff = Stuff & {
    // This is now applicable and must always exist
    fromEarth: boolean,
};

// Error because false cannot be a boolean AND a nullable boolean simultaneously
const moonRock: EarthStuff = {
    name: 'moon rock',
    fromEarth: false,
};
```

### Exact Props

By default, flow allows "wide typing".
This means it ignores extra props that are not expected in the type.

Exact props are used to avoid this, to ensure that extra props are not overlooked.
But intersection types on exact props doesn't work well.
This is probably because the intersection of an exact object means that the value must satisfy **all of** the
intersected objects while not violating the exact prop constraint.
Since the purpose of intersection was to DRY the props, this is clearly not desirable.

# Destructuring Subtyping

## Benefit

The benefit of destructuring is that you can avoid the recursive property intersection behaviour.
This allows for clobbering props completely.

```js
type Stuff = {
    name: string,
    fromEarth: boolean | null,
};

type EarthStuff = {
    ...Stuff
    // Completely replace original type declaration
    fromEarth: boolean,
};
```

# Conclusion

I think we want to only use destructuring approach, as there is a hard blocker on using exact props.
Exact props are very useful, so this is a severe limitation.

The dream would be to to use intersection syntax (explicit, even if it's only syntactic sugar) and have objects
intersect with a union behaviour.
