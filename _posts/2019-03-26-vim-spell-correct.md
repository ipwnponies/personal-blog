---
title: Vim Spellcheck Keybinding
categories:
- programming
tags:
- vim
---

Vim has spellcheck capability but it's awkward to use.
When`spell` option is set, typos are highlighted in vim.
The `z=` is used for spellcheck suggestions and replacement.
It triggers a menu that lists many suggestions, ranked in terms of relevance.

It would be very convenient to have keybinding that replaces typo on the fly, without interrupting the writing flow.
This translates in vim-speak to an "insert-mode mapping that picks the first spelling suggestion and returns cursor
back in insert mode".

# Mapping

This is the magical incantation we need:

```vim
inoremap <C-l> <c-g>u<Esc>[s1z=`]a<c-g>u
```

What a doozie.
Let's unwrap it, piece by piece.

1. `inoremap <c-l>` sets an insert-mode binding to ctrl-l.
1. `<c-g>u` "commits" the current change, while remaining in insert-mode.
 Any additional text is the start of the next change in the undo tree.
 This sets a mark that allows us to return the cursor to.
1. `<esc>` swtiches to normal mode. We used this since it's noremap, and cannot use our normal binding of `jk`.
1. `[s` moves backwards to the previous spelling error.
1. `1z=` replaces the word with the first choice in spelling suggestion.

<!-- markdownlint-disable MD038 MD032 -->
1. `` `] `` returns the cursor to the point where `ctrl-l` was invoked.
<!-- markdownlint-enable -->

1. `a` enters insert mode.
1. `<c-g>u` "commits" the text replacement we just did.
 Now, undo will reverse spelling suggestion.
 Undo again, will undo the first bit of typing.
