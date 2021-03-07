---
title: Fizzbuzz As A Programming Interview Problem
categories: programming
tags:
  - interview
---

I used to use [fizzbuzz][wiki] for programming interviewing purposes.
There's going to be strong opinions regarding this and I think it'll be interesting to present my case.

[wiki]: https://en.wikipedia.org/wiki/Fizz_buzz#Programming

Nowadays, I do "structured" interviewing and I wasn't involved in the original inception of the problems.
But maybe these points can be thought-provoking for what you should value within an programming interview problem.

## Problem Statement

Fizzbuzz is a simple toy program.
For the numbers 1-100:

- print "fizz" if the number is divisible by 3
- print "buzz" is the number is divisible by 5
- else print the number

The output is expected to look like:

```ignore
1
2
fizz
4
buzz
...
...
98
fizz
buzz
```

## Arguments For Why This Is A Shit Problem

I'm going to play devil's advocate here, as I've heard many common complaints about the validity of this problem.

### This Is A Contrived Problem And Doesn't Represent Real Day-To-Day Work

The sentiment of this is admirable.
A position for a database admin should not be testing you on HTML and CSS.
A frontend developer role should not test you on machine learning.

You want to ask reasonable questions within your domain and it's clearly aligned if you choose actual problems your
team has had to solve in the past.
But... I really hope you don't literally use day-to-day work problems in interview settings.
Is the work you do so trivial that you can completely explain it and I can solve it within the 60 minute we share together?
What do you do the rest of the time and should I be concerned that your work is not interesting and challenging to me?

Or did you pick a real-world problem that has taken you 20 minutes to explain and has taken me another 20 minutes to
gather sufficient implied context?
Forgive me for being a little slow, I wasn't embedded on your team for last 6 months so I have a little catching up to do.
You must have terrible communication skills if you can't target your audience and reduce the problem to their working knowledge.

Fizzbuzz is contrived but that isn't mutually exclusive with it being interesting problem to solve.
Your problem is also contrived, it just happens to have a few flavour elements sprinkled in to make it seem applicable.

### It's Trivial, This Is Insulting To A Candidate's Intelligence

Fizzbuzz is trivial, you say?
Then why do I see &lt;70% success rate at solving this problem in 45 minutes?
This is excluding the 5 minutes it takes to explain.

It's trivial in that it's clear to explain and there are no hidden tricks.
None of that bullshit about expecting you to further clarify the problem, it's very clear what the problem is.

### How Do We Get Any Signal

How do we get signal?
Well, managing to pass the problem is literally a huge signal.
Once we get past that bare minimum, there are ways to extend this problem to collect signals in many areas, don't
worry about that.
If you think this problem lacks opportunity to gather more signal, you're limiting your imagination.

## Arguments For Why This Is A Good Problem

### Aggressive Filtering

Fizzbuzz has, anecdotally, been very aggressive at filtering.
Scarily so, like 50% of the time a candidate clearly struggles to this trivial problem and I guarantee it would be
unanimous among interviewers that it does not meet the bar.
There are no tricks here, it's acts as a minimum bar.

This follows the [pareto principle]: 80% of the signal will be achieved with 20% of the effort.
I can try to get signals from many different angles but does that matter if the bare minimum is not passed?

[pareto principle]: https://en.wikipedia.org/wiki/Pareto_principle

If they solve this trivially, it takes &lt;10 minutes.
Great, we now have 35 minutes remaining and I have a read of their level.
We get right into harder problems and begin to collect more signals from different aspects.

### It's Trivial To Understand

Fizzbuzz is dead easy to understand.
Both parties understand the expected input and output.

Time is limited in an interview and squandering it on problem set up feels unfair to the candidate.

When I see a candidate, it might be the 5th or 10th interview round they've had in the last two weeks.
Am I going to be that special-snowflake that thinks his problem is super important, interesting, and relevant to the candidate?
Nah, we both know this game, I'm trying to suss out whether you have the stuff and you're trying to show me the goods.
Let's be respectful to each other and try to get as far as possible along the most optimal path.

### It's Incremental

So you solved fizzbuzz in 5 minutes and are insulted at the triviality.
How is this interviewer going to fill up the 40 minutes?
Bam, additional requirements.

Wait that's not fair!
Real life requirements are set in stone.
We never refactor and maintain code.

/sarcasm

#### Parametrize 3 And 5, Refactoring And Extensible Code

Next step is allow another user to change "fizz" to divisible by 2 and "buzz" to divisible by 7.
Okay... can they support both use cases?
You can already see this requires parameters.
It also means you can't hardcode values.
Both of which... are good programming practices.
This is literally what 50% of our jobs involve, extending or rewriting code!

Here, I hope to see the use of default parameters, which provides backwards compatibility for first use case.
Our first user shouldn't need to change anything just because we decide to release a minor version update.
Is the code extensible?
If it wasn't originally, no biggie, we avoid pre-optimizing in real life.
But being to adapt is what is useful.

#### Parametrize Fizz And Buzz, Code Design And Architecture

Next is to change the words "fizz" and "buzz".
Can they extend it to couple "fizz" to 2 and "buzz" to 7?
Relying on positional args isn't elegant.
Will they come up with a data structure that captures it (tuples works)?
Wait, does that allow it to take variadic input?

All this demonstrates design and architecture skills.
Yes, there are edge cases.
I let the candidate reason it out and play the part of a PM.
I can be negotiated with, as long as your final code fulfills our agreed requirement.
If a number is divisible by more than one input and you tell me you want the precedence of concatenation to be
left-to-right, that's fine!
But did you think of this and did you clarify this ambiguity to the PM?
In the real world, we find out shit all the time, as we start implementing.
"Joe, we can do it two ways. The first is simpler but doesn't handle negative numbers, is that okay?"

Here I'm gauging how they work with ambiguous requirements.
This catches many candidates off-guard, as they expect to be told what to do exactly.
And, unfortunately, this is also the case with many full-timers.
Here I'm gauging collaboration and communication skills.
I'm gauging ownership and gusto.
Really take advantage of my willingness to let you mold the problem.

#### Change 1 To 100 Range

Yet another refactor.
This usually surfaces broken assumptions and off-by-1 errors.
Debugging skills!

Do they handle invalid inputs?
If I swap the order of lower and upper bound around, because I am bad code writer, what does the program do?
I don't really care about correctness, I want to see how you think and respond when I tear apart your code.

### Testing

Still here?
How do we prove this works?
Unit tests!

#### Test Range

The actual unit tests are not important but I'm looking for what edge cases the candidate has considered.
Are they testing the complete range 1-100?
We don't always have that luxury with complex code.
And that's a lot of values to assert.

Can they decompose the range into subsets that are more orthogonal and can give each a good test case name?
i.e. `test_fizz`, `test_buzz`, `test_fizzbuzz`, `test_number`

Can I test range 20-30?
It's a more reasonable range of 10 numbers to assert.

#### Print To Console

Did they just print to console?
This is typical and it's fine.
But it's untestable.

Astute readers will know to refactor logic to a testable function, one that returns lists of ints.
Then the original function prints the list to console.
We skip testing the original function because it's not worth getting test coverage for.
But the inner function is highly testable.

I've seen candidates suggest to capture stdout and do string parsing.
This is misguided but it's not a bad signal.
It needs a hint in the right direction, to channel that energy.

Even with the refactored code, I've seen candidates that did not know to assert portion of the return.
Calling `fizz_buzz(1,100)` should get 100% testing coverage in a single test case, this guy needs like 6.

### Types And Interface Design

Remember how we print "fizz", "buzz", or the number?
When we return a value, what is the type?
Some candidates coerce to string and that's great to hear them explain why they prefer consistent typing.

Others keep the two types and I want to know why they think that's advantageous.

If indifferent, this is a signal of inexperience.
I try to impose statically typed languages onto them and ask how they would resolve.
This hinting is usually enough to spur discussion or thought.

### Language Agnostic

I was once told that the candidate had not written code in years and they had done mostly systems administration recently.
Pretty sure that was a bad call to apply to a posting that requires coding and to be hired without any ability to
demonstrate this.

Regardless of this ill-thought through plan, I persevered and offered to help in whatever language they were
comfortable with.
Actually writing code is only 20% of the interesting signal.
I think they believed they could cop out by saying `bash` and therefore this problem did not apply.
I really needed some signal or else it's defacto no, which was unfortunately the case here.

After that call, I was annoyed that they wasted both our time and set out to prove them wrong.
Thus, this gist with fizzbuzz written in `fish` and `bash`.
I intend to fill it in further with more esoteric and useless languages, just to prove this point.
The point that they were a baddie and trying to hide behind a shell-scripting language.
I happen to be a well-versed in shell-scripting languages and I know that &gt;90% of people don't even know basic
constructs such as looping and conditionals.
Anyone can namedrop languages into their resume.

<!-- markdownlint-disable MD033-->
<script src="https://gist.github.com/ipwnponies/33f48cc03665a289055e158f20130ca7.js"></script>
<!-- markdownlint-enable MD033-->

## Summary

I hoped I was able to bring some credence to fizzbuzz as a programming interview problem.
When people show disdain for this problem, I really want to know why?
Are they just parroting what they've been told or do they have valid arguments?
Just parroting back what you've been told is just like reusing code or design patterns because you heard it was good practice.

I love using fizzbuzz as it's a counter to the other programming interview problems:
fizzbuzz is not complex and doesn't require data structures or algorithms to solve.
It requires good programming foundations to be able to explain all the nuances of a solution for this trivial problem.
It's basically leetcode-proof.
This shit would be leetcode baby-mode.
I have great disdain for leetcode pros whose only skillset is the ability to solve leet code problems, really fast.
I don't work at leetcode so their skills are worthless to me, I need software engineering skills.
