---
title: When Python 3 Cannot Handle Unicode Encoding
categories:
- programming
tags:
- python
- unicode
- arm
---

I deployed my [youtube playlist script] to my C.H.I.P. so that I could set up a weekly cronjob.
The code is highly portable, not depending on many libraries and not the types of libraries with binary dependencies.

[youtube playlist script]: https://github.com/ipwnponies/youtube-sort-playlist

I ran it and it proceeded to blow up.
Because it would be surprisingly if a deployment to a new untested system would ever work the first time (thank god for containerization).

```python
Traceback (most recent call last):
  File "playlist_updates.py", line 384, in <module>
    main()
  File "playlist_updates.py", line 380, in main
    youtube_manager.update(args.since, args.only_allowed)
  File "playlist_updates.py", line 284, in update
    self.add_channel_videos_watch_later(channel['id'], uploaded_after)
  File "playlist_updates.py", line 239, in add_channel_videos_watch_later
    self.add_video_to_watch_later(video_id)
  File "playlist_updates.py", line 242, in add_video_to_watch_later
    print('Adding video to playlist: {}'.format(video_id['title']))
  File "/home/ipwnponies/youtube-sort-playlist/venv/lib/python3.6/site-packages/tqdm/_tqdm.py", line 526, in write
    fp.write(s)
UnicodeEncodeError: 'ascii' codec can't encode character '\u2019' in position 52: ordinal not in range(128)
```

Wait wut?
Is this python 2?

```sh
$ python
Python 3.6.8 (default, Apr  6 2019, 18:53:42)
```

Nope, it's 3.6 that I freshly installed through pyenv.

# Testing Against a Working Environment

Let's switch to my desktop and set a control test in a known working environment:

```python
$ python
Python 3.6.5 (default, Apr  1 2018, 05:46:30)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print('\u2019')
’
>>>
```

And on the C.H.I.P.:

```python
$ python
Python 3.6.8 (default, Apr  6 2019, 18:53:42)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print('\u2019')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode character '\u2019' in position 0: ordinal not in range(128)
```

# Locale

After soul searching on google for answers, I found my prayer. On my desktop:

```python
$ python
Python 3.6.5 (default, Apr  1 2018, 05:46:30)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.stdout.encoding
'UTF-8'
```

But the C.H.I.P. is not utf-8...

```python
$ python
Python 3.6.8 (default, Apr  6 2019, 18:53:42)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.stdout.encoding
'ANSI_X3.4-1968'
```

Python determines the encoding based on the terminal.
I was unsuccessful in determining the exact criteria and it's also poorly documented.
But it decided that I didn't have UTF-8 support available.

The correct fix is to set the `LC_CTYPE` environment variable to 'en_US.UTF-8'.
`LC_ALL` can also be set if you want to change the language option universally.

But my locale was already set:

```sh
$ locale
LANG=en_US.UTF-8
LANGUAGE=
LC_CTYPE="en_US.UTF-8"
...
```

So what's the deal?

# PYTHONIOENCODING

At this point, my interest has rapidly waned and I was searching for a solution.
You can set `PYTHONIOENCODING` to explicitly tell python what to use.

```sh
$ env PYTHONIOENCODING=utf-8 python
Python 3.6.8 (default, Apr  6 2019, 18:53:42)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print('\u2019')
’
```

# Conclusion

None of this shit makes sense to me and it's not well documented.
I found a chain of complaining, from [macfreek] to [code monk], and I'm going to tack on my grievances to this.

[macfreek]: http://www.macfreek.nl/memory/Encoding_of_Python_stdout
[code monk]: https://drj11.wordpress.com/2007/05/14/python-how-is-sysstdoutencoding-chosen/
