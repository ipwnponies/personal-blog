---
title: Color Wheel
categories:
- technology
tags: []
---

I watched this [video on youtube][1] from the *Technology Connections* channel, discussing the colour brown.
It was extremely fascinating.

[1]: https://youtu.be/wh4aWZRtTwU

The colour brown is unique in that it's a distinct colour but is actually just dark orange.
Colour is cultural so I'm speaking from the perspective of North American and English-descended languages/cultures.

Let's visit some fundamentals of colour theory to establish the proper terminology.

## Colour Models

We need to talk first about [colour models][2].
This refers to the mathematical model to describe individual colours.

[2]: https://en.wikipedia.org/wiki/Color_model

There are several common models used day-to-day:

- RGB
- CMYK
- HSL

These models are built on the basis of how the human eye works.
The eye has different types of receptors that are sensitive to red, green, and blue wavelengths.
These colour models take advantage of human perception and the post-processing performed by the brain.

This means non-human entities could possibly see different outputs, if they were sensitive to wavelengths different from
RGB.
It's like a hash function, there are different inputs that produce the same output.

### RGB

RGB is a model where colours are described as values of red, green, and blue.
This is commonly used in web design and computer programming.

It is an additive model, where values of 0 represent zero light.
This makes it map directly to displays, where LEDs of each colour emit light and computers control the amount to form colours.
The contribution of luminosity of each colour contributes to the final perceived colour (additive).

### CMYK

CMYK is a model where colours are described as values of cyan, magenta, yellow, and black.
Ignore black for now and we'll explore the relationship to RGB.

This color model is made up of the complementary colours of RGB:

- **red's** complementary is the combination of green and blue, **cyan**
- **green's** complementary is the combination of red and blue, **magenta**
- **blue's** complementary is the combination of red and green, **yellow**

CMYK is a subtractive model, which starts from white and removes wavelengths.
RGB is an additive model, which starts from black and adds wavelengths.

Computer displays produce light and are conducive to RGB (additive model).
Printed material absorbs some wavelengths of white light and reflect the remainder (subtractive).
When pigments are mixed together, you're adding materials that will absorb a wider spectrum of wavelengths, resulting
in a darker colour.
Mix all the pigments and all the colours are absorbed, resulting in black

#### Black

Why is black in the CYMK model?
In theory, there would be no need for black pigment.
In practice, mixing together cyan, magenta, and yellow results in a dark, muddy colour.
There's some reflection as it's imperfect.
A black pigment is used to directly address this.

Also, in the printing industry, it's common to print black text.
A separate black pigment allows for unbalanced ratio in a printer, one that favours a larger reservoir.

### HSV

HSV is a colour model where colours are described with hue, saturation, and brightness values.
See wikipedia for more [detailed description][5].

[5]: https://en.wikipedia.org/wiki/HSL_and_HSV#Color-making_attributes

Hue is the angle on the colour wheel.
Customarily, 0 degrees is red, yellow is 60, green is 120, cyan is 180, blue is 240, and magenta is 300.

Saturation is "colourfulness" of the colour.
How deep the colour is.
At full brightness, changing saturation would make a bright red become pastel, faded red.

Brightness is how much light is being emitted.
How dark a colour is or the dimming of other wavelengths.
At full saturation, changing the brightness would make a deep red become a darker red.
A pink could become a darker pink.

[4]: https://youtu.be/wh4aWZRtTwU?t=405

## Brown

Back to brown.
In color model speak, brown is orange with decreased brightness value.
In HSV, if you keep hue pinned to orange (30 degree), at full saturation, then lowering the brightness will reveal brown.

Brown is a unique, distinct colour in culture but mathematically, it's "dark-orange".
We have "dark-blue", "dark-red", "dark-yellow", but a unique and assigned name for "dark-orange".
Sure there are names we give, such as "navy blue", "maroon", "tan" but those are aliases for their equally understandable
"dark-" variants.
Except "dark-orange", which I presume many people would do a double-take.

How we interpret brown vs. dark orange is based on context (contrast with surroundings).
Seriously, watch 30 seconds of the [video][3].
The video has a brown square on a black background.
The background fades to white and the colour appears to change from brown to "darker orange".
It's real trippy.

[3]: https://youtu.be/wh4aWZRtTwU?t=474
