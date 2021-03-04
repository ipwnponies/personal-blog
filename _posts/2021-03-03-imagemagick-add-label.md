---
title: Adding Labels Using Imagemagick
categories: technology
tags:
  - images
  - tools
---

Years ago I wanted to edit a video clip, add a label, and make a gif.
I wrote about it in this [gist].
I'm revisiting it now and posting it for discoverability.
Surprisingly, I can still understand what I wanted to do!

[gist]: https://gist.github.com/ipwnponies/0d00f5d6ce1ee335fafc339a7fc3dca6

This was to add "hello world" label onto the gif, while slowing it down in the moment.
It was used for a blooper shot, so the slowdown was more dramatic effect and annotated as such.

Anyhoo, here's the original post.

---

## Summary

Imagemagick is hard to use and the documentation/tutorials available are not intuitive.
Here is a concise explanation of what needs to be done to edit a gif to add labels.

## Code

<!-- markdownlint-disable MD013-->

```sh
convert foo.gif \                                                            # Specify the original gif
-gravity center -pointsize 30 -font ComicSans \                              # Set font position and styling
-duplicate 1,0-20 \                                                          # Clone frames and append to the end (clone frame once)
'(' -clone 21-40 -fill white -annotate -0-150 'Hello' -set delay 6 ')' \     # Clone frames, add 'Hello', and slow down gif delay for only these frames
-duplicate 1,41-89 \                                                         # Clone frames and append to the end (clone frame once)
'(' -clone 90-120 -fill white -annotate -60-50 'World' -set delay 4 ')' \    # Clone frames, add 'World', and set delay
-delete 0-120 \                                                              # Delete the original frames
foo_output.gif                                                               # Output file
```

<!-- markdownlint-enable MD013 -->

## Notes

- `convert` is the imagemagick command that is used to modify gifs
- `-gravity` is used to set the position of the text. This is what x y offsets are relative to
- frames are either duplicated or cloned+modified, appending them to the existing gif and control ordering.
  `-delete` is used to remove the original frames
- `-duplicate` will copy the frame range and append to the end.
  This is memory-efficient way to clone frames (imagemagick only copies reference frame upon write) but doesn't allow modification
- `-clone` requires imagemagick's parenthesis scope. Modified frames are appended to the end

## Reference

[`convert` reference](https://www.imagemagick.org/script/convert.php)

[Frame-by-frame modification](https://www.imagemagick.org/Usage/anim_mods/#frame_mod)
