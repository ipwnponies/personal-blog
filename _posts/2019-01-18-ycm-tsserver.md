---
layout: default
title: Setting Up YouComplete with Javascript Completion
---

# Motivation
I wanted to setup autocompletion for javascript.
Turns out that it's not as simple as it is for python.

VS Code uses typescript language server to provide completions.
There seems to be a movement towards implementing completion server through a common protocol,
instead of one-off integrations (YouCompleteMe and jedi, for python completions).

# YouCompleteMe
I use YouCompleteMe (YCM) for completions.
YCM uses a plugin based architecture, which where completion server integrations are setup.
```shell
ls -1 ~/.vim/bundle/YouCompleteMe/third_party/ycmd/third_party/
argparse/
bottle/
cregex/
frozendict/
go/
gocode/
godef/
jedi/
JediHTTP/
OmniSharpServer/
parso/
python-future/
racerd/
requests/
tsserver@
waitress/
```
Many of were probably installed as part of ycm `./install.py --all` step.
`tsserver` is not, we'll need to manually set this up with a symlink.

## Configuration
YCM allows plugins to provide diagnostics.
This term seems to be the as showing errors in the linting and type checking world.

This feature is to provide compatibility for Syntastic but we use ALE for linting.
In this case, there might not be much value and we'll be getting many errors due to `tsserver` incompatibility with flow.
You can either disable ycm diagnostics (by turning off the appropriate values) or filter out the known error messages, using `g:ycm_filter_diagnostics`.
```vim
 let g:ycm_filter_diagnostics = {
             \   "javascript": {
             \     "regex": [
             \         "^.* can only be used in a .ts file.$",
             \         "^Duplicate identifier 'type'.$"
             \     ]
             \   }
             \ }
```

# Typescript
Microsoft has separated VS Code from the completion server that powers javascript completion.
This language server provides both completion and type checking.
For my purpose, I was only interested in the completions, as I relied on `flow` and `ALE` to perform type checking.

`tsserver` can be installed directly via `npm install typescript` (must be inside YCM `third_party/`).
Or you can install it wherever and set up a symlink.
Once installed you can verify it's working by running `:YcmDebugInfo` and checking to see if `TSServer` process is running.
```
Printing YouCompleteMe debug information...
...
...
-- TypeScript completer debug information:
--   TSServer running
--   TSServer process ID: 10094
--   TSServer executable: /Users/ipwnponies/.vim/bundle/YouCompleteMe/third_party/ycmd/third_party/tsserver/bin/tsserver
--   TSServer logfiles:
--     /tmp/tsserver_gl4uxgxk.log
--   TSServer version: 3.2.2
...
...
```

# Setting up your Javascript Project
`tsserver` looks for a `jsconfig.json` file and uses the configurations to know what to parse.
A minimal config looks like this:
```json
{
  "compilerOptions": {
    "target": "es6",
    "checkJs": false,
    "baseUrl": ".",
    "paths": {
        "*" : [ "*" ]
    }
  },
  "exclude": [
    "node_modules"
  ]
}
```
Option | Description
| - | -|
target | Version of ecmascript to target
checkJs | Set to true to enable typescript type checking
baseUrl | The filepath that is the root to javascript files
paths | Set the mapping for imports. The key is the import path in code and value is the relative filepath from `baseUrl`.
exclude/include | These are glob patterns for files to include or exclude. It's important to exclude extraneous dirs like node_modules, which will greatly slow down the engine.

# ALE

## Type Checking
I use flow for typing but `tsserver` does not support this.
Probably makes sense, they want you to use typescript.
ALE is aware of `tsserver` and will use it if available.

We want to blacklist `tsserver` from ALE linting for flow files.
In javascript filetype plugin (`~/.vim/after/ftplugin/javascript.vim`), set the linters to ignore:
```vim
let b:ale_linters_ignore = ['tsserver']
```
`:ALEInfo` doesn't really indicate this well, even looking like nothing worked.
But when you run `:ALELint`, internally ALE will not run `tsserver` and this is apparent only when you inspect the output messages.

## Completion
Because `tsserver` is a language server, it provides ALE with completion and linting functionality, overlapping some features with YCM.
Since I'm wanting to use completions with YCM, we want to disable ALE completion.

This is the default setting (`g:ale_completion_enabled`).

Strangely, `:ALEGoToDefiniton` command worked right out of the box for me.
So this might be useful for initially debugging that your project is configured for `tsserver` consumption.

## Overlapping Tools and the Future
It'll be interesting to see how the landscape changes over the next few years, with Language Server Protocol (LSP)
standardizing the interface for language servers.
It's possible these two tools will converge, as the scope of handling external integrations is reduced to the same source.
