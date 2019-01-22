I've wanted to do more blogging.
No real direction or idea, just thought it would be nice to have a place to put down my thoughts on things I discover day-to-day.
At the moment, it's likely to either be cooking or programming related.
For either, use of formatting is important and will be used often:
* recipes will have warnings, ordered instruction steps, pictures, and links to other sites
* programming will have links to documentation, code snippets, and downloads

Github Pages allows free hosting (obviously with sensible limitations, such as traffic volume, content size, etc.).
My use fits their use case very well:
* I don't have traffic.
* I want to use markdown, for easy authoring that can be done anywhere.
* I am terrible with UX and web design.

# Setting up github pages
I created a repository and went to the repository settings to enable github pages.
It's pretty straight forward and their docs served me well.

# Jekyll
Github pages uses `jekyll` for setting up website.
There's a lot to take in but it's essentially a declarative templating language.

## Types of pages
There are 3 types of pages:
* pages
* posts
* collections

Pages are regular pages in a site directory.
Other than organizing them in a directory hierarchy, these don't have special handling.

Posts are meant to be used for blogging.
These have datetime in the filename. i.e. `2019-01-21-foo.md`
You create posts under a `_posts` directory.

Collections are used to organize multiple pages into common groups.
I might use these to separate cooking and programming pages apart.

## _config.yml
`_config.yml` is the file where site configs and defaults are configured.
Defaults can be configured to only apply to specific filepaths or collections.

## Liquid
Liquid is the name for the formatting language.
It's processed by Jekyll when building the page.
This is how conditional or array maps are created.

## Front Matter
Front Matter is the header at the top of pages that is used to configure settings.
These values can be set on the page or in `_config.yml` as a global default.
The values are used by the Liquid, on the page on layout, for formatting.

# Minimal Mistakes Themes
The 8 themes native to Github Pages didn't really catch my eye.
I found the [`Minimal-mistakes`](https://mmistakes.github.io/minimal-mistakes/) theme and it was very slick.
It has different layouts and many customizable extras.
I was drawn to this theme because it supports a table of contents, based on markdown headers.

I don't plan on writing long blogs but why wouldn't you want navigation by headers?
I guess most people write single, long-form blog entries.

## Installing the theme
To install custom theme, you set the `remote_theme` property in `_config.yml`.
It takes a github repository.

The gotchas I encountered was not including the `jekyll-include-cache` plugin.
Turns out github pages includes some plugins (or whitelists them for use when required by theme).
This is documented but I didn't read carefully.
It causes jekyll to fail to build.

## Setting the default layout for blogs to single
The other gotcha was that the `default` layout is not used directly in this theme, it's the base class for layouts to build on top of.
The `single` layout is the one that's recommended for a blog post.
All my existing blog posts needed to be updated from `default` to `single`.

Instead to explicitly setting the layout every time, we can set up the default for `_posts` to use `single` layout.

In the `_config.yml`, set the `defaults` property:
```yaml
defaults:
  # _posts
  - scope:
      path: ""
      type: posts
    values:
      layout: single
      author_profile: true
      read_time: true
      toc: true
      toc_sticky: true
      toc_label: On This Page
```
This sets the default values for posts. Like in Hiera (puppet), it's the analogous to the `common.yaml`.
Now we don't have to repeat ourselves when files are in the `_posts` directory!
