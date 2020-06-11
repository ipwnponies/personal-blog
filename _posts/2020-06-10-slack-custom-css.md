---
title: Slack Custom CSS
categories:
- programming
tags:
- slack
- customization
---

The Slack desktop app is an [Electron app][1], a framework for developing distributing web applications.
Electron is a stripped-down web browser, powered by Node runtime and Chromium engine.
Because it's inherently a web browser, we can apply our web knowledge as the undocumented API.

[1]: https://en.wikipedia.org/wiki/Electron_(software_framework)

## Where to Inject

I'm no expert at Electron but I know that you can append javascript code to `/Applications/Slack.app/Contents/Resources/app/dist/preload.bundle.js`.
It will be executed automatically when application runs.

## What to Inject

Here is a `fish` script I hacked together to automate injection.
Every time Slack updates, it's possible that the injected file will be clobbered.
So this script is useful for quickly reapplying changes.
You can even hook it up to be shadow your Slack app!

This requires [asar][2], which is the Electron archival format.
Install this once and use it to extract the electron `asar` to a directory.
Electron apps will prefer to use the expanded directory if it exists (citation required but it definitely works).

[2]: https://github.com/electron/asar

```sh
#! fish

# Add path which contains nodejs, asar
set -l current_dir (dirname (status filename))
set PATH $PATH:$current_dir/node_modules/.bin/

set slack_root_dir /Applications/Slack.app/Contents/Resources

# Specify font with ligature support
set font 'Operator Mono Lig'

function customCss
    # Customise your CSS styling here!
    echo "
        code, pre, code, pre {
            font-family: \"$font\" !important;
            font-size: 13px;
            font-variant-ligatures: common-ligatures;
        }
    "
end

function unpack_if_required
    if not test -d $slack_root_dir/app
        asar extract $slack_root_dir/app.asar $slack_root_dir/app
        mv $slack_root_dir/app.asar{,.bak}
    end
end

function patch_if_required

    set -l entry_bundle $slack_root_dir/app/dist/preload.bundle.js
    if not test -e $entry_bundle
        echo 'Entry bundle not found, slack app must have updated! Please fix this script'
        exit 1
    end

    if tail -n 1  $entry_bundle | not grep -q '//patched'
        set css (customCss)
        set PAYLOAD "
            document.addEventListener('DOMContentLoaded', function() {
              let customCss = `$css`;
              var styles = document.createElement('style');
              styles.appendChild(document.createTextNode(customCss));
              document.head.appendChild(styles);
            });
            //patched
        "

        echo 'Patching...'
        echo $PAYLOAD >> $entry_bundle
    else
        echo "PATCHED"
    end
end

function check_asar
    if not type -q asar
        echo "Please install asar: npm install -g asar"
        exit 1
    end
end

function main
    check_asar
    if not test -d $slack_root_dir
        echo "You don't have Slack installed"
        exit 1
    end

    unpack_if_required
    patch_if_required
end

function font_validate --no-scope-shadowing
    set font $_flag_value

    if system_profiler SPFontsDataType 2>&1 | not grep -q $font
        echo \"$font\" is not an installed font. Check your spelling
        return 1
    end
end

argparse 'h/help' 'f/font=!font_validate' -- $argv

# Font flag is required
# No positional param allowed
if not set -q _flag_font; or test (count $argv) -ne 0
    set _flag_h 1
end

if set -q _flag_h
    set -l filename (status filename)
    echo "$filename: Injects code into the Slack bundle for the purposes of setting CSS styling"
    echo '-f/--font <font>'
    exit
end

main
```

## How to Debug

Slack uses a environment variable to enable debug mode.
In this mode, you can right-click and "inspect" the DOM.

On OSX, this is:

```sh
env SLACK_DEVELOPER_MENU=true open -a Slack
```
