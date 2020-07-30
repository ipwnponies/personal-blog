---
title: Thought Experiments
categories:
- thinking
tags:
- thought experiment
---

I watched a video from [*TopTenz*][1] that discussed 10 thought experiments.
I found it very fascinating and wanted to give my thoughts.

[1]: https://www.toptenz.net/10-thought-experiments-that-will-mess-with-your-brain.php

## Plank of Carneades

This a [thought experiment][2] first proposed by an ancient Greek dude.
It explores the idea of murdering in self-defense.

[2]: https://en.wikipedia.org/wiki/Plank_of_Carneades

### Thought Experiment - Plank of Carneades

There are two sailors, *A* and *B*, who are involved in a shipwreck.
They both swim towards a floating plank.
*A* arrives first and it becomes evident that the plank will only support a single person.
*B* pushes *A* off, knowing full well that they would drown.

When *B* is saved, can they be tried for murder?
Or can it be considered murder for the purpose of self-defense?

### My Thoughts - Plank of Carneades

This scenario is set up such that the two individuals are not directly adversarial but indirectly.
This thought experiment can be applied to a less contrived self-defense situation,
where a home owner kills a burglar (castle laws).

We'd like to believe that *B* would sacrifice themselves, accepting their death and that *A* fairly came first (first-come-first-serve).
But how different is this from the home defense situation?
Should *B* murder *A* in self-defense or should *B* sacrifice themselves (let the burglar burgle)?

In the real world, we use common-law, traditions, or rote process to establish precedent and avoid thinking about this.
For example, there's a [tradition of the captain going down with the ship][3].
Even if saving the ship or its passengers seem hopeless, the captain is expected to remain to the bitter end.
They cannot abandon ship and argue self-defense, with this thought experiment.

[3]: https://en.wikipedia.org/wiki/The_captain_goes_down_with_the_ship

## Library of Babel

This [thought experiment][4] is a short story from an Argentinian author.
It touches on the idea of infinite or definite.

[4]: https://en.wikipedia.org/wiki/The_Library_of_Babel

### Thought Experiment - Library of Babel

There is a library that is made of seemingly infinite galleries.
In the galleries, there are books that contain all different permutation.
Given a finite character set (letters and punctuation), is there an end of the library or is it infinite?

### My Thoughts - Library of Babel

I don't find this one too interesting.
It requires suspension of disbelief to allow for "seemingly indefinite" books.
That's where it immediately becomes not so compelling anymore.

I think the thought experiment might be interesting to others, if they question the concept of free will.
Any book you want to write will have already existed.
We can reduce this down to a countable set, such as a 5-sentence paragraph, where the longest line is at most 20 words.
It's possible to produce all permutations such that you cannot write a unique "free-will" sentence
that does not already exist.
But even something this constrained, has a massive key space.

## Two Generals' Problem

This [thought experiment][5] was first conceived when discussing network communications.
It discusses the impossibility of guaranteed reliable communication.

[5]: https://en.wikipedia.org/wiki/Two_Generals%27_Problem

### Thought Experiment - Two Generals' Problem

Two generals of the same army are planning to attack a fortified city.
They are on opposite sides of the city, which is nestled in a valley.
They must coordinate their efforts, to successfully flank and breach the defenders.

In order to communicate, a messenger must be sent and they must go through the valley.
There is always a chance of the messenger being captured en route.
Since the generals each know they need to coordinate, they will only move when they are certain the message was
successfully delivered.
So they expect an acknowledgement of delivery from the other general.

But this acknowledgment message itself can be intercepted, which means the second general cannot be sure that
the first general knows to follow through.
We can see how it will require infinitely recursive acknowledgement messages from both sides,
in order to come to a consensus, short of omnipotence.

### My Thoughts - Two Generals' Problem

This thought experiment is used to illustrate the impossibility of 100% guaranteed delivery in a communications network.
We instead design systems to always be able to tolerate potential loss:

- Use of sequence id when sending a message or its acknowledgement, allows the recipient to convey to the general what
they most certainly know
- Sending multiple redundant messengers, to greatly reduce the possibility of having all messages captured
- Agreements, established before deploying to the field, on retriability or keep-alive pings,
as a way to signal absence of communications

I don't have any thoughts to add beyond what smart people have already talked about.
Communications are not 100% reliable, this situation is unlikely but not impossible.
Being naive in implementation can lead to a bad time.

## Famous Violinist

This [thought experiment][6] came from an essay "A Defense of Abortion".
It discusses the ethics and perspectives surrounding abortion.

[6]: https://en.wikipedia.org/wiki/A_Defense_of_Abortion

### Thought Experiment - Famous Violinist

One morning, you wake up in great pain and in an unfamiliar place.
There's a person whose back is right next to yours.
A man comes in to explain that the person was dying and they've kidnapped you to save their life.
This person was of great importance, a famous violinist.
Through surgery, you're now sharing the kidney function.
If you wait 9 months, the person will have recovered enough of their own kidney functionality to survive on their own.

You can choose to tough it out for 9 months or you are in your rights to demand a separation.

### My Thoughts - Famous Violinist

The analogy here is very blunt and not disguised at all.
The thought process is that you're already here, what choice do you make for the future?

Waiting it out for 9 months is an act of kindness you're bestowing on the violinist.
But you carry all the potential risks:

- reduced quality of life and opportunity cost
- risk of losing kidneys (thing on loan is lost)
- risk of complications due to prolonged exposure (earlier is safer than later)

I'm not going to comment on the real world use of this because it's not an area that I have any meaningful
to provide or any knowledge.
This thought experiment is not very subtle, it's directly substituting a famous violist in place of a fetus,
perhaps to introduce new perspective and work around preconceived biases.

## Experience Machine

This [thought experiment][7] comes from a philosopher and discusses hedonism.
*Hedonism* is the philosophy of striving for maximal pleasure, regardless of other factors.

[7]: https://en.wikipedia.org/wiki/Experience_machine

### Thought Experiment - Experience Machine

Imagine a machine that could give whatever desirable or pleasurable experience a user wants.
The designer's of the machine have also figured out a way so a user cannot distinguish the experience in the machine
versus the real world.
However, once plugged in there is not way to revert this operation and return to the real world.

Knowing you could live a fake life full of pleasure and wonder, would you give up the real world?

### My Thoughts - Experience Machine

This thought experiment is meant to provoke thought to dispute the validity hedonism.
On paper, there's no reason a rational human-being wouldn't take the offer.
But when you think about it, there's a human element in the thought process that doesn't take kindly to
giving up the flawed, but real, world.
That means that humans are hedonistic, pleasure is just one of many factors that we are all striving to
maximize in our pursuit of happiness.

The [Matrix][8] and Black Mirror's [San Junipero][9] immediately come to mind.

[8]: https://en.wikipedia.org/wiki/The_Matrix
[9]: https://en.wikipedia.org/wiki/San_Junipero

In the Matrix, the protagonist begins the story already in the machine.
But there's a constant feeling under the surface, a curiosity, of a another world out there.
Even though the protagonist isn't in a shitty situation, they are compelled to continue to seek out this world,
by virtue of it being more real.
Morpheus even gives the protagonist the direct option to continue living in the Matrix by taking the blue pill,
an act of accepting and returning to the embrace of hedonism/abandoning curiosity.
The antagonist Cypher directly addresses this in the *steak* scene, where he acknowledges the steak is not real
but he is all about that hedonism.

San Junipero is about two elderly people, who visit a virtual world.
Your thoughts can be preserved and uploaded to this world but this process is invasive and your physical form will die.
Its use in the show is for hospice care, to indefinitely extend the lives for its users.
In this world setup, why would you wait until your physical body passes?
If this simulated world was just as good, or even better, why not expedite the inevitable process?
What is the human element that makes this seemingly straight-forward decision muddled?

I believe these hesitations (for me at least), point to dispute the argument that humans are hedonistic.
It's not only about the destination (feelings and pleasure) but includes the journey.
It helps to not think of money, as it's a reward with no upper bound for desired target.
Imagine poor college students seeking out free food, for some the quest is the pleasure they derive and not necessarily
the mediocre cold pizzas as the reward.

## Spider in the Urinal

This thought experiment comes from a philosopher and discusses the consequences and outcome of altruism versus inaction.

### Thought Experiment - Spider in the Urinal

One day, you walk into the bathroom to use a urinal and see a spider.
When you flush the urinal, the spider clings on for dear life.
Everyday, it continues to remain here and not able to escape.
But the urinal provides sustenance in the form of water.
And it struggles to cling on with every flush.

Seeing that this miserable existence, you use some paper towel to let the spider move onto and you place the paper
towel on the floor.
The next day, the paper towel and spider are still there but it is now dead.

### My Thoughts - Spider in the Urinal

This is a thought provoking concept, to counter the naive assumption that your altruism is always the best for all.
Others will value other things and you can never really understand what that is.

The "suffering and miserable existence" of the spider is your own interpretation.
The spider may have highly-valued being close to water, so much that it was willing to suffer the flushes.
And your altruism left it in a worse-off position.

My takeaway is not much more than: "don't think you know what's best for someone, give them that choice to reach the
same conclusion".
Our altruistic tendencies can sometimes be paradoxical: the best outcome is to let someone suffer (from our perspective)
because that's what they want.

The classic stereotype is when young, middle-upper class, and typically white, American students go to
developing countries to volunteer to build houses.
The outcome for the locals is not great.
They are a flood of cheap labour, directly competing with the livelihood of local tradesmen.
Or the houses produced are low quality and require follow-up work, unnecessarily increasing the final cost.

Or when people attempt to support non-local agricultures, such as fair-trade quinoa.
As a result, this puts market pressures to convert a staple food to becoming a [cash crop](https://en.wikipedia.org/wiki/Cash_crop).
Surely we can see that nobody intended to buy quinoa as a way to make food availability an issue for locals and
increase the stress and suffering.
They altruistically wanted to reduce exploitation, to increase the quality of life for people in that region.

In both cases, the intentions are pure and altruistic, no doubt about that.
But no one cares about your intention, the outcome is real and lasting fallout must now be dealt with.

## Swampman

This is a [thought experiment][10] that discusses what it means to be human, the intangible elements.

[10]: https://en.wikipedia.org/wiki/Swampman

### Thought Experiment - Swampman

Lightning strikes a dead tree in a swamp, while you're standing nearby.
Your body is reduced to elemental molecules while the tree is transformed into a physical replica.
The swamp thing returns home, seems to recognize your friends, greets them, and moves into your house.
No one can tell a difference.

Is the swamp thing you?
Is it at least a person?

### My Thoughts - Swampman

This is similar to the transporter in Star Trek, where the an exact replica is made at the destination and
the original source is killed.
This trope is played out in the *Prestige*.

It's similar to the [Ship of Theseus][11] thought experiment.
If you replace enough parts of the ship, when does it stop being the same ship?
Or is the ship an intangible concept, with the identity supplanted onto the new parts?

[11]: https://en.wikipedia.org/wiki/Ship_of_Theseus

This thought experiment makes us question what it means to be a person.
We know it's more than just the physical materials, as humans replace cells, grow and change, dye our hair, etc.
This is a common trope in comic books involving clones: even if the thoughts were cloned, are they the same person?
Or have you spawned a new identity and now have two instances?

## Kavka's Toxin Puzzle

This [thought experiment][12] is a paradox and involves some game theory.

[12]: https://en.wikipedia.org/wiki/Kavka%27s_toxin_puzzle

### Thought Experiment - Kavka's Toxin Puzzle

A billionaire places a vial of toxin that will cause you grain pain but will not threaten your life.
If you tell the billionaire at midnight, that you intend to drink this tomorrow afternoon, he will pay you monies.
You are free to change your mind tomorrow but you can keep the money.

### My Thoughts - Kavka's Toxin Puzzle

This paradox hurts my head.
A reasonable person will intend to drink, as that results in an award.
This award outweighs the downside, it's not debatable that it's a better deal.

If you intend to drink this, there's no reason for you to back out tomorrow afternoon.
You already know all the rules so it's impossible for you to truly intend to drink it but back out at the last second.
You can't intend to drink and also intend to not drink tomorrow simultaneously.

So you must follow through and drink.
But a rational person would reevaluate on the next day: why am I drinking this, I know I got paid and I know I can back out.
To follow through at this stage would be irrational, as no further gain can be had by drinking the toxin.
Other than following through on a previous commitment, one that no one else cares about any more.

## Survival Lottery

This [thought experiment][13] discussed utilitarianism.

[13]: https://en.wikipedia.org/wiki/Survival_lottery

### Thought Experiment - Survival Lottery

Imagine if there is a survival lottery.
When drawn, that person will be expected to sacrifice their life.
Their organs will be donated to many others.

### My Thoughts - Survival Lottery

This is very interesting thought experiment.
If 5 patients are awaiting organ donations, letting them knowingly die is not different then actively killing someone.
The sacrifice of the one will net more lives saved overall.

It is the complete and total sacrifice of the few for the greater good of the many.

I see this as the progenitor for the phrase "all things in moderation".
A completely utilitarian system is cold and calculating.
Efficient and rational but deeply unsettling.
It lacks emotional touch.

In real life, this happens in group dynamics, such as ordering food for a party.
If one person is vegan, should they be expected to eat second-rate food choices?
Or should everyone eat vegan as well, to accommodate the common denominator?

In practice, we know that it's neither extremes.
Have a dish or two that is vegan and not a second-thought (falafels).
The vegan should expect not to be able to eat most of the other dishes.
In the gruesome thought experiment, real life plays out like a donor donates some organs and accepts a lower quality of life.
Some patients are saved and others do not find a donor in time.

## Roko's Basilisk

This [thought experiment][14] discussing information hazard.

[14]: https://en.wikipedia.org/wiki/LessWrong#Roko's_basilisk

### Thought Experiment - Roko's Basilisk

Imagine there is a yet-to-be-conceived AI.
When it comes into existence, it will find those that knew but did not help bring it into existence and punish them.
Do you help bring this AI into existence, to stay on its good side?
Or do you ignore it or actively prevent it?

### My Thoughts - Roko's Basilisk

This is the classic example of information hazard.
I don't know why this story needs AI, I though Jehovah's Witnesses were a real-world example of information hazard.
Something about when rapture happens, only the good will be saved.
But that cannot happen until everyone has been made aware and had a chance to be a good person.
If a remote tribe in the Amazon Rainforest does not know about this, then rapture cannot happen.

So knowing this is an information hazard, as you're now part of the game.
You can help be a good person by spreading the word, which will bring about rapture.
But you will be spared.
Or you could actively prevent it, by protecting remote tribes from contact, thereby indefinitely delaying rapture.
Either way, you no longer have neutral position to stay default to.

Information hazard comes up a lot in security and privacy.
By limiting what you tell others, you spare them from information hazard.
For example, by limiting who has access to a company's financials, you can limit unintentional insider trading.
Being ignorant of someone else's action lays no fault to you.
Being made aware now forces your hand, usually due to personal ethics and moral.
Inaction is not a choice, you'll be complicit by virtue of being responsible to society.
