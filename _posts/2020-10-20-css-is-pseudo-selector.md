---
title: "CSS :is() pseudo-selector"
categories: [programming]
tags: [css]
---

The [`:is()` pseudo-class function][1] is a selector that acts as a boolean `OR`.
It's blazing hot, fresh out of the oven:
it's only available on modern browser from 2018+.
As of today (2020-10-20), it appears to be on all modern browsers but will probably require polyfill for the next few years.

[1]: https://developer.mozilla.org/en-US/docs/Web/CSS/:is

It's value is in reducing duplication in query selector.
Previously, if you want to match all `span` and `p` under `#foo`, you would use a [*selector list*][2].
This is a comma-separated list of independent selectors.
In this case, the duplication is that `#foo` will need to specified twice:

``` CSS
#foo span .target,
#foo p .target {}
```

[2]: https://developer.mozilla.org/en-US/docs/Web/CSS/Selector_list

Replace `#foo` with a more complex query, one that involves 4 or 5 `:nth-child()` and you can see that copy-paste is
less than optimal.

Enter `:is()`.
It can be used to specify descendent queries in an `OR` fashion.

``` CSS
#foo :is(span, foo) .target {}
```

Look at that, we were able to increase the candidate set of an ancestor.
And it reads very clean.

Personally, I think my common use case for this will be writing custom user styles or greasemonkey scripts for sites
that have nonsensical structures.
I find that in those cases, I am unable to anchor on a target element by id.
And end up using many `:nth-child()` calls to navigate the tree.
