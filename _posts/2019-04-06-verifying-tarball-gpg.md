---
title: Verifying Downloads With GPG
categories:
- programming
tags:
- security
---

Many open source projects will provide pre-compiled binaries for convenience.
They are often signed with gpg key and provide a checksum.
Why do all of this?
Let's learn a little about security and best practices.

# Why Sign Files

Pre-compiled binaries contain executable code.
You should not run executables from an untrusted source.
How do you trust the source?

Just because it's hosted on their website doesn't mean it's not susceptible to malicious intent:

* An attacker may upload a similarly-named package as a mirror.
* Someone could modify the file in transit, maybe the attacker is in control of the network.
* An attacker may have control of the hosting server.

Signing files prevents all these.
When a file is signed, it generate a signature file, which can be freely distributed.
Generating the signature file requires access to the private key, which provides for user authentication and trust.
An attacker cannot modify the file and generate an accompanying signature because they don't have access to the key.
The signature file is literally a stamp of authority and trust, in both time and space.
From that point onwards, it's possible to verify the file that was signed is the same file file as the author intended
to distribute, how matter how many hands it passes through or how much time has elapsed.

# Checksum

A checksum is used for file integrity checks.
It hashes the data and you can use this to see if the file has been tampered with.

This should not be used to test trust, as it only provides integrity check, not authenticity.
There are no private components in a checksum, it's possible for an attacker to tamper a file and provide an updated
hash, if they had control of the hosting server.
Or if they were a hosting mirror and masquerading as the original source.

Because importing and trusting private keys is such an involved process, checksum can serve as a lightweight check for
things that don't require that much scrutiny.
i.e. If I'm installing an esoteric, niche program that will run with elevated privileges, I should verify digital signature.
But if not and it's only going to run on a separate dummy user anyways, we can use checksum as a sanity check.

The attacker would need to exploit the niche site (possible) to serve the tampered files and updated checksum.
Their return would be a clean-slate sandbox.
And the number of affected users would be in the dozens.
What I'm trying to illustrate, and justify, is that using checksums as a convenient proxy for security can be
acceptable, depending on the circumstances.

# Digital Signatures

Using `gpg` can be unintuitive, if you only look at the user flow without understanding the philosophy behind the web of
trust.

This [blog post][kamarada] does a good job of going through the steps.

[kamarada]: https://kamarada.github.io/en/2018/11/08/verifying-data-integrity-and-authenticity-using-sha-256-and-gpg/

## Add Trusted Keys

The first thing to do is add a key for a trusted person.
They'll advertise their public key, which are uploaded to <http://keys.gnupg.net/> and makes is easy to install.

```sh
gpg --recv-keys <KEY>
```

This will prompt you to install the public key.
It's possible to specify the different levels of trust you have but I'm not sure what that feature is used for.

Normally you wouldn't blindly add keys from strangers over the internet.
For real hardcore security, you would meet the person directly and exchange keys physically.
That way, there's no way confusion on whose identity you're verifying.
There are even [key signing parties], where people meet in person and exchange keys.
This works towards a web of trust, where you trust someone and therefore can trust the identity of their acquaintances
and so-forth.

[key signing parties]: https://en.wikipedia.org/wiki/Key_signing_party

## Verifying a Digital Signature

Signature files are `.sig` or `.asc` files.

```sh
gpg --verify foo.tar.gz.asc
```

`gpg` will read the signature file and verify that the signed file was indeed signed with the private key of the author.

I won't go into details but this relies on public-private key cryptography.
Only the private key could have been used to generate the signature that only the public key can read.
