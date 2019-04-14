---
title: Windows Task Scheduler
categories:
- programming
tags:
- windows
- automation
---

Windows Task Scheduler can be used to schedule tasks to run at a specific time of day.
It's the equivalent of `cron` on unix.
Unfortunately, the interval scheduling is not as flexible as `cron`.

While WSL has `cron`, using a native scheduler does have its benefits:

* Can wake a computer from sleep with hardware wake timer (ACPI S3 state)
* Disable task if on battery
* Delete task automatically if not run after a time period
* Only run if the computer is idle
* Trigger on OS events, such as log in, wifi connect, an event, etc.

# Wake Timer

A task can be triggered to wake up from sleep with a hardware timer.
This is great for my personal desktop, where I put it to sleep to turn off the fans and monitor.
When a task is triggered, it wakes the computer up, runs, and then the idle timeout puts the computer back to sleep.

# Importing and Exporting

Tasks can be exported to XML format, either in the UI or with `schtasks`.
With `schtasks`, you can output in different formats: table, list (json-like), or CSV.

Unfortunately, this command is so poorly designed:

* There's a *verbose* flag that must be used to output more information.
  Not more tracing. But actual relevant information.
  This flies in the face of Unix program conventions, where `-v` is used for debugging.
* The outputs for each format are varying columns.
  I mean, what the shit, shouldn't they just be different views into the same data set?
* When exporting to xml, all the tasks are grouped as collection of tasks, in a single valid xml file.
  But you can only import single tasks.
  You literally cannot import the very things you just exported, a direct violate of *Reversible Actions* in UX design.
  Who thought this made sense.

# Learnings

## Don't Use Repeat Interval

There's a feature that allows repeat runs once triggered.
I initially thought I could set up a daily trigger, with hourly repeats, to run a script hourly during working hours.

But this is a gotcha.
Only the initial time has a wake timer scheduled.
The repeat intervals don't have wake timers, which means they only run on a schedule but cannot wake from sleep.
I'm not sure what a use case would be for this behaviour, when you can simply schedule more, first-class tasks.

To do this, I exported the task, then used `sed` to generate multiple files for each hour I want to schedule.
Then you can use another command to bulk import tasks.

## Custom Time Values

The UI is poor and has bad UX.
All the dropdowns, with limited list of options for 5, 10, 30 minutes, etc, are actually editable.
You can actually set these values to custom values that will get parsed.

If you export the task to XML, you can see that under the hood it's an [ISO-8601 repeating interval][1].

[1]: https://en.wikipedia.org/wiki/ISO_8601#Repeating_intervals
