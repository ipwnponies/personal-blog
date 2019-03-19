---
title: Including Files in Jekyll
categories:
- programming
tags:
- blog
---

`Jekyll` wants to be a blogging-first platform.
For reasons I don't know why.
Blogging as a primary feature is fine and all but I don't see why the architecture and design needs to be constrained
to force everything to work in blogging context.

They seem unwilling to implement features that make it useful for general purpose website development.

I want to write recipes and iterate on them with learnings.
These recipes would belong in a collection as non-blog pages.

I want to write a blog post that includes the snippet.
And every time I try the recipe again, I will write another post and include the same recipe.
The blog post will take about the experience, which I want to capture at that moment in time.
If I have a bad recipe from the start, I don't want to have it persist.

# How-to

Here's how you include a file from a collection:

{% raw %}

```liquid
{% assign recipe = site.recipes | where: "title",  "Ramen Noodles" | first %}
{{recipe.content}}
```

{% endraw %}

This will find a page in the *recipes* collection with the matching title.
Then we include the page's `content`.

## Example

{% assign recipe = site.recipes | where: "title",  "Ramen Noodles" | first %}
{{recipe.content}}
