---
title: Prime Rib with Chimichurri
categories:
- cooking
tags:
- recipe
- roast
- beef
---

I made prime rib for the first time this Christmas.
It was pricey and lots of a meat for a single person to eat but I really wanted to embark on this experiment.
These are some of the learnings I picked up.

## Prime Rib

For cooking the prime rib, I used the ["reverse-sear" method][1].
Reverse sear is where the meat is slowly brought up to temperature and then seared in an hot oven at the end.
This technique contrasts with the conventional approach of initially browning the meat before roasting it.

[1]: https://www.seriouseats.com/recipes/2009/12/perfect-prime-rib-beef-recipe.html

The main advantage is that it's similar to sous-vide, where the gentle heat transfer results in even cooking.
The large time window can be forgiving for adjusting and course-correcting.

---

{% assign recipe = site.recipes | where: "title",  "Prime Rib" | first %}
{% include recipe.html page=recipe %}

---

### Calibrating oven temperature

Since I moved to a new oven setup, I wasn't sure how the oven behaves.
I made the mistake of using this roasting instance to test the oven's temperature accuracy.

For calibrating an oven, you can use water in a pyrex bowl for temperature less than 212F/100C.
For hotter temperatures, use a high-temp oil.
Due to heat transfer slowing down as temperature differential is smaller, it will take a long time to get a true read.
Something like 2+ hours to each final temperature.
During this team, the variable you're dealing with can be heat loss due to evaporation, which can keep the water
temperature depressed and give low reading.
This was the mistake in my approach.

I set the oven temperature and measured the temperature after 20 minutes.
These are the the readings:

Set temperature (F)| Measured Temperature (F)
-|-
180 | 135
200 | 145
225 | 155
250 | 165
300 | 175

As you can see, there's a large gap in measured temperature and set temperature.
However, I didn't wait 2+ hours to get a true read.
I know for a fact that foods will brown at 350F/180C in this oven, so that's definitely much hotter than <200F.

After all this, I can safely say it's way easier to get an oven thermometer instead.
They're very inexpensive, <$10.

## Chimichurri

I didn't make an au jus to eat the prime rib with but I decided to go with chimichurri instead.
Chimichurri is a sauce that [comes from Argentina][2].
It's commonly eaten with grilled meats.
It's basically a cousin to pesto and other herb-oil sauces.

[2]: https://en.wikipedia.org/wiki/Chimichurri

The primary ingredients of chimichurri are: parsley, garlic, oil, oregano, chili flakes, and wine vinegar.
You can add whatever else you'd like but the main flavour profile is garlicky, chili, and herbaceous.

---

{% assign recipe = site.recipes | where: "title",  "Chimchurri" | first %}
{% include recipe.html page=recipe %}
