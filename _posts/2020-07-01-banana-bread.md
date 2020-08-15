---
title: Banana Bread
categories:
- cooking
tags:
- recipe
- baking
---

I'm finally getting around to writing down a banana bread recipe.
I've been burned by not maintaining my own canonical recipe, with preferences and tweaks.
In particular this time, the recipe was way under seasoned... because it probably assumed table salt was to be used.

Here's hoping to incrementally better banana breads in the future!

BTW, is the difference between a quick bread loaf and muffins just the shape of the container?
Perhaps the muffin allows for crown development while the loaf is amenable to slathering of butter.

---

{% assign recipe = site.recipes | where: "title",  "Banana Bread" | first %}
{% include recipe.html page=recipe %}
