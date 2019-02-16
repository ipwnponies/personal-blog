---
title: Using AppleScript to Connect to Bluetooth Headset
categories:
  - programming
tags:
  - apple
  - automation
---

I learned how to use AppleScript to write a macro that would connect to a bluetooth headset (airpods).
AppleScript is a scripting language for MacOS that can be used to automate UI things.
I'm using it to click through menu items for me automatically.

# General Design

Scripts can be written in applescript or javascript.
I found applescript to be easy enough to grok and pick up, given enough examples.

OSX menus are designed in a tree hierarchy.
You can navigate down the tree specifying menu items by index, title, or with a filter.

Method | Example
-|-
Index | menu item 1
Title | menu item "AirPods"
Filter | menu item whose title "Airpods"

# OS Menulet

```applescript
activate application "SystemUIServer"
tell application "System Events" to tell process "SystemUIServer"
        set btMenu to (menu bar item 1 of menu bar 1 whose description contains "bluetooth")
        tell btMenu
            click
            tell (menu item "AirPods" of menu 1)
                click
                if exists menu item "Connect" of menu 1 then
                    click menu item "Connect" of menu 1
                    return "Connecting..."
                end if
            end tell
        end tell
end tell
```

# Third-Party Menus

The menu bar at the top consists of OS and third-party menu items.
OS menu bar items belong to `SystemUIServer` process.
Items such as bluetooth, battery, volume, etc.

Third-party menu items are accessed through their respective processes, as `menu bar 2`.
`menu bar 1` is the main menu bar when the application is active: file, window, format, help.

```applescript
tell application "System Events" to tell process "Alfred 3"
    set alfredMenu to menu bar item 1 of menu bar 2
    tell alfredMenu
        click
        set toggle to menu item "Preferences..." of menu 1
        click toggle
    end tell
end tell
```

## Gotchas

From my observations, most applications' menu bar 2 will only have a single menu bar item, the icon.
The other gotcha I discovered was that the menu items for third-party apps are lazy loaded, unlike OS menu items.
This means you need to click the menu bar and wait for `SystemUIServer` to refresh.
Only then can you access the menu items of sub-menus.
