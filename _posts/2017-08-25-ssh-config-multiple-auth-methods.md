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
gssapi-keyex |
gssapi-with-mic |
