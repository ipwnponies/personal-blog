---
layout: default
title: SSHD Multiple Authentication Methods
---
# Setting Up an SSH Server with Multiple Authentication Method
## Motivation
Let's set the scene:
- You manage an ssh server
- You want to whitelist users by their public key (`public-key`)
- Those users can only access from a whitelist set of machines (`hostbased`)
- We'll ask them to answer some silly questions for our entertainment (`keyboard-interactive`)
  <sup id="ref1"><a href="#footnote1">1</a></sup>

## How to do this
The required authentication methods are configured in `sshd_config` with the `RequiredAuthentications` setting.
The value is a comma separated list, in the order that authentication will be evaluated.
The possible choices are:

Auth Method | Description
-- | --
password | Type in password
keyboard-interactive | Type in text, sent over the wire for ssh server
publickey | Public-private key encryption
hostbased | Authorizes clients from specific hosts
gssapi-keyex<sup><a id="ref2" href="#footnote2">2</a></sup> | [Generic Security Services API](https://en.wikipedia.org/wiki/Generic_Security_Services_Application_Program_Interface) using key exchange
gssapi-with-mic | GSS API using MIC tokens

We'd probably configure our ssh server as such:
```
RequiredAuthentications2 hostbased,publickey,password,keyboard-interactive
```
This will require the user to ssh from a whitelisted host, use their ssh key, enter their password,
and answer our silly monkey question.

## Debug
To verify that this is configured probably, you should see the following in the output
when you `ssh -v`:
```
debug1: Authentications that can continue: keyboard-interactive
```
---
<sup id="footnote1">
  A more real-world use of this would be to implement two factor authentication
  <a href="#ref1" title="Jump back to footnote 1 in the text.">↩</a>
</sup>
<sup id="footnote2">
  This is a protocol for providing an authentication service, such as Kerberos.
  Truth be told, I have troubles comprehending this so this is just going to be my random ass guess:
  gssapi allows deferring the authentication to another service.
  <a href="#ref2" title="Jump back to footnote 2 in the text.">↩</a>
</sup>
