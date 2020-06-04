---
title: Interplay of RSA and Diffie-Hellman
categories:
- programming
tags:
- cryptography
- computer science
- technology
---

Diffie-Hellman and RSA are two related concepts in cryptography.
A common misunderstanding are the roles that the two play.
An often asked question is:

> Can I just use RSA to encrypt a message, do I really need diffie-hellman?

Once you understand, you'll realize there's no need to answer because it's asking the wrong question to begin with.
Sure you can hack it to "work" but that's sort of working by coincidence.

## Key-Exchange

Key-exchange is the concept of safely exchanging a shared key between two parties.
This is done without either party needing to flat-out reveal their secret.

They [do this][diffie hellman key-exchange] by generating and publicly sharing a common value.
Independently, they mix in their secret to this common value and send it over.
Upon receiving this partial secret, they add in their secret and now have the same keys, without having sent the keys.

[diffie hellman key-exchange]: https://security.stackexchange.com/a/45971

### Analogy With Colours

1. Alice wants to share a key with Bob.
    - She is *red*, Bob is *blue*
1. Alice tells Bob to use the colour *green*.
    - Carol was eavesdropping and knows about *green*.
1. Alice mixes *green* with *red* and gets *brown*
    - She gives it to Bob
    - Carol knows about *brown*
1. Bob mixes *blue* into brown and gets... *something*.
    This is the shared key.
1. Bob mixes *green* into *blue* and get *teal*.
    - He gives it to Alice
    - Carol knows about *teal*
1. Alice mixes *red* into *teal* and gets... *something*.
    This is the shared key.
1. Carol tries to figure out how *green*, *brown*, and *teal come together.

Carol is the man-in-the-middle.
She hears everything but is never exposed to Alice or Bob's actual secrets.

She can't decompose the colours to derive the secrets either, that's the hard part (maths).

And she can't simply mix *brown* and *teal* together to get *something*.
This is a weakness in this analogy because colours can be mixed.
Because they contain pigments from Alice and Bob's secrets.

In practice, these are numbers and math operations.
There is not math operation for mixing these values.
Nor is there a math operation for decomposing (factorization).

## Public Key Infrastructure

RSA is public key infrastructure.
It serves to establish trust and authentication.

A public and private key-pair are generated.
They have mathematical and cryptographic properties that allow them to complement each other.
It is mathematically hard to derive one from the other, besides brute force.

The user can freely share the public key, which allows others to encrypt messages.
These messages can only be decrypted by the private key.

In the other direction, the user can encrypt with the private key and only users with the public key can decrypt.
Since everyone has access to the public key, the point is not encoding the message:
rather, it's proof that this message is authentic and came only from the user, since it requires a private key.
Customarily, the user would use the private key to **sign** instead of encrypt.
The payload would not be encrypted but other users would use the digital signature to verify integrity.

## RSA and Diffie-Hellman

So how do the two work together?
We need to exchange a key in order to start sending messages.

But it's trivial for Carol to sit in the middle and intercept all messages.
If all messages proxy through Carol, she can exchange keys with Alice and independently with Bob.
When Alice sends a message, Carol will decrypt (Alice's shared key), tamper, and re-encrypt (Bob's shared key).
[Oh no!][diffie hellman mitm]

[diffie hellman mitm]: https://stackoverflow.com/a/10496684

Key exchange is great way to avoid sharing secrets, when creating a shared key.
It does not handle the issue of authentication.
You need to be sure who you're performing key-exchange with.
While you might not leak your private secret, you'll just communicate directly with the attacker!

You need public key infrastructure to authenticate.
As a part of key-exchange, Alice will use Bob's public key to encrypt the secret values.
Even if Carol is in the middle, without Bob's private key she cannot know what the values are.
Nor can she simply respond and complete key exchange to Alice.

### Why Not Use Rsa For Everything

This begs the question of why do we even need a symmetric key (output of key-exchange).

Asymmetric encryption is slow.
This boils down the algorithm.
It performs a lot of exponentiation and modulo to encrypt, which requires several cycles in the CPU arithmetic
processing unit.
While symmetric is XOR, which is trivial bit operation (with some fanciness, like chaining blocks).
So fast, orders of magnitudes faster.

We also don't want to use RSA too often.
It's expensive to establish initial trust, it needs Certificate Authority or physical public key exchange.
This makes it very onerous to revoke and issue new keys.
Which means we reuse the same public/private key for a long period.
Whereas key-exchange is trivial, we should generate these per-sessions.
Using different key each time is *Perfect Forward Secrecy*:
if a key is cracked, previous sessions are still protected as they all use different keys.

Use RSA for authentication.
This defends against masquerading, man in the middle.
It prevents Carol from injecting, can only observe traffic.

Use diffie-hellman to exchange keys without requiring either party to disclose any secrets.
This protects either party, in case one of their keys is later compromised.
