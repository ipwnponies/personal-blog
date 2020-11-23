---
title: Markov Chain Text Generation
categories: programming
tags:
  - computer science
---

When you read about computers generating text, such as a chatbot or AI-generated book/research papers, you might have
heard the term _Markov Chains_.
Let's dissect this concept and use some analogies to demystify it.
There are many foreign terms surrounding that make the base concept much more complicated than it really is.

During a hackathon, I played around with the [markovify] python package and [generated _Dragon Ball Z_ subtitles][dbz-markov].
Before embarking on this project, I had little idea what _markov chains_ were and I needed very little understanding to
get this working.

[dbz-markov]: https://github.com/ipwnponies/dbz-markov-faces
[markovify]: https://github.com/jsvine/markovify

## What Is A Markov Chain

A [_markov chain_][wiki] is:

> a stochastic model describing a sequence of possible events in which the probability of each event depends only on
> the state attained in the previous event

This is a long winded way of saying it's a state machine that is random:

- it's a FSM due to the sequencing of events aka moving between states
- it's stochastic (random and time driven), rather than event-driven

[wiki]: https://en.wikipedia.org/wiki/Markov_chain

## Markov Chain Text Generation

How is this useful for text generation?
Languages have grammar constructs that result in patterns.

> I (subject) want (verb) salsa verde (direct object) with my tacos (indirect objects)

In English, this is [subject-verb-object order][svo-wiki].
You can't change this without sounding like Yoda.
This means we can find many patterns of _I_ leading to _want_, and _want_ leading to _salsa_ or _tacos_.

[svo-wiki]: https://en.wikipedia.org/wiki/Subject%E2%80%93verb%E2%80%93object

We can create a finite state machine, where each node represents a word and the next state leads to the next word.
To move within the state machine, we do not use events but assign probabilities to each edge.
The probability is the frequency of the next word.
This is a [_markov chain text generator_][wiki-text-generator].

[wiki-text-generator]: https://en.wikipedia.org/wiki/Markov_chain#Markov_text_generators

We can seed the chain by analyzing texts, called a _corpus_.
The more words in the corpus, the more nodes and edges we will have.
This will give more pathways when generating text and may produce more fluid sentences.

We can feed it a subset of related texts, to reinforce patterns among domain subjects.
In my case, I feed it _Dragon Ball Z_ dialogue, which we all know has a lot of common tropes.
This resulted in very successful output and was realistically believable to be actual dialogue from the show.
