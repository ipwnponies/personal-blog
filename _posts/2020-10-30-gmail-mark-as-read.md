---
title: Make gmail unread count useful again
categories: programming
tags:
  - automation
---

Ever since Google killed Inbox (rip), I've been unable to find a way to fill that void in my workflow.
Inbox let you batch together emails into bundles, which is serviced by labels and filters in Gmail.
I wouldn't complain if it weren't so much more work in Gmail, while frictionless in Inbox.

You're supposed to archive emails in your inbox, regardless of whether you read them or not.
This is how you get to "inbox zero".
This works fine in gmail.

But it doesn't mark them as read.
And there's only an unread count for a label, not a "count in inbox".
So if you don't mark them as read... how do you know how many unread emails you have for each label?
A singular value for total _unreads_ in the inbox is not very useful: some labels have higher intrinsic priority than others.

My workaround is to continue my workflow but use automation to automatically mark emails as read.
This drives the unread count number down to the actual value.

## Manually marking as read

It's not hard to find emails that have been archived but not read.
Aka emails I have read but don't care to look into the contents of.
Simply search `-in:inbox is:unread`.
Select these emails and _mark as read_.

That's the manual step and is very tedious if you expect me to run it every 5 minutes.

## Script

Enter Google Apps Script.
It's a scripting platform for many Google products, such as _Sheets_, _Docs_, and _Gmail_.
One thing to note is that it uses an old-ass version of Javascript.
Like from 2010.
I'm not sure why they haven't updated it, it's like a relic of the past.
I seriously spent 30 minutes stuck because I had the audacity to use a modern feature, such as `const`.

After we write our script and grant it permission to read and mark emails, we can set it up to run automatically every
5 minutes.

Here's a [complete example][1].

[1]: https://www.labnol.org/code/19712-mark-archived-gmail-read
