---
title: Window Lock Screen With Idle Timeout
categories:
- programming
tags:
- windows
---

# Lock Your Computer

At a workplace, it's good practice to lock your computer when left unattended.
It's easy for a bad actor to quickly open a backdoor.
Or data leak, if you're in a position of privileged information.
It doesn't even need to involve leaking secret projects or product launches:
  it can even be financial reports before public earnings call, risking inviting insider trading.

It's common to lock the computer when laptop lid is closed or as soon as computer goes to sleep.
And it's equally common to allow a short grace period (30 seconds), where the computer remains unlocked.
In case it was a user error.

# Home Computer

For my home computer, my attention is not 100% on the computer as it would be at work.
I might use the computer to see a recipe and am idle in between cooking steps.
As such, it quickly becomes very annoying to unlock the computer every 5 minutes.

Instead of 30 seconds grace period, I want something more extended, say 1 hour.
If I'm away from my desk for more than 1 full hour, one can assume that I'm no longer nearby!
Perhaps I am completely preoccupied with a different task or watching a movie.
Or I've left altogether.

There isn't an immediate solution for this in Windows 10 but I found a working solution.

# Windows 10 Task Scheduler

*Windows Task Scheduler* can be set to trigger a screen lock upon these idle conditions.

## Command

The following is the command to trigger a manual lock:

```shell
rundll32.exe user32.dll,LockWorkStation
```

## Trigger

Use the *On Idle* trigger.
This will trigger this task upon computer idle.

## Condition

Conditions are where we add more idle conditions.

Set the task to start when the computer is idle for "1 hour".
This is a string which is somehow magically interpreted.
Follow the pattern from the presets.

Set "wait for idle" to "Do not wait".
This config value is confusing to decipher but this [post explains it][1] with a good example.

1. When any of the trigger events fire, these idle conditions are further evaluated.
1. If not yet idle, "wait for idle" up to the max time.
    If timeout, then don't run the task.
1. Once idle, wait until minimum required idle time is reached.
1. Run task.

[1]: https://superuser.com/a/777494

There are other options that are self-explanatory:

- Abort the "countdown" if the computer is no longer idle
- Do not resume "countdown" if resumes being idle.
    There is no accumulation of idle time.
