---
title: Including Markdown in Jekyll
categories:
- programming
tags:
- jekyll
- markdown
---

For this blog, I wanted to write recipes and refer to them in blog posts.
The blog posts are static and won't change but I will continue to iterate on recipes as I refine them.

I could link to the recipe but I thought it would cool to dynamically embed the content of the recipe automatically.

# Embedded Recipe Template

I want a template that I can easily reuse.
I'm going to refer to the same recipe over time and I'll be writing new recipe posts as well.

This can be done using [jekyll's includes][1] functionality.

[1]: https://jekyllrb.com/docs/includes/#passing-parameters-to-includes
{% raw %}

```liquid
{% assign recipe = site.recipes | where: "title",  "Bread Pudding" | first %}
{% include recipe.html page=recipe %}
```

{% endraw %}

The first statement finds the correct recipe in the collection.
The second statement passes the page to the include template.

The include template looks like this:
{% raw %}

```liquid
[{{include.page.title}}]({{include.page.url}}):

<div style="border-radius:5px;border-left: 6px solid #cccccc; background-color: #f5f5f5">
{{ include.page.content | markdownify }}
</div>
```

{% endraw %}

This template adds a link to the canonical embedded recipe.
Then the contents of the page are wrapped in a styled div, so that it's clear that there's a section of the page that
comes from elsewhere.

Note that we need to pass the content to `markdownify`.
`Liquid` variables are escaped so they need to be sent through jekyll's `markdownify` filter to unescape them again.
