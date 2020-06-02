---
title: AppleScript to Toggle Natural Scrolling
categories:
- programming
tags:
- osx
---

I recently tried using a mouse at my work station, instead of Magic Trackpad.
OSX has a setting for *Natural Scrolling* behaviour, which is the opposite for mouse scroll behaviour.
The purpose is that it lends itself to a more intuitive behaviour with trackpads:
swiping downwards scrolls upwards.

This sounds strange and the opposite.
Think instead physically moving tactile sheets of paper:
sliding the sheet downwards brings the upper portion into view.
This is why it's coined as *Natural Scrolling*.
I really like this, it means the trackpad behave as a first-class input device, as opposed to a proxy for a mouse device.

Unfortunately, there's only a single global setting and this means **all trackpads and mice** share the same behaviour.
There are apps ([karabiner][1]) that allow for customization but I found this [stackoverflow post][2]
with an AppleScript to automate toggling the mouse settings.

[1]: https://karabiner-elements.pqrs.org/
[2]: https://apple.stackexchange.com/a/264742

```applescript
on run
  try
   tell application "System Preferences"
      set current pane to pane "com.apple.preference.mouse"
      activate
    end tell
    tell application "System Events" to tell process "System Preferences"
      set cbValue to value of (click checkbox 1 of window 1)
    end tell
    tell application "System Preferences" to quit
    tell me
      activate
      if cbValue is equal to 1 then
        display notification "Natural scrolling is now active."
      else
        display notification "Natural scrolling is no longer active."
      end if
    end tell
  on error eStr number eNum
    activate
    display dialog eStr & " number " & eNum buttons {"OK"} default button 1 ¬
    with title "Toggle Natural Scrolling" with icon caution
  end try
end run
```

Note that this needed a small update for Mojave (10.14), probably because the mouse preference layout was changed.
