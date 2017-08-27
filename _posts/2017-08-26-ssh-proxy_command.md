---
layout: default
title: SSH Proxy Command
---
# SSH Proxy Command

## Motivation
A proxy command is a command that is run before establishing an ssh connection.
The connection to jumpbox is handled transparently behind the scenes.
There is some nuance when using a proxy command in jumpbox scenario in that you need to handle stdin
and stdout appropriately, otherwise it can get swallowed.

## OpenSSH 5.4
Prior to OpenSSH 5.4, you needed to use netcat as the ssh command:
```
ssh -o ProxyCommand='ssh jumphost.example.org nc %h %p' remotehost
```
When you try connect to remotehost, you will first ssh to the jumphost and open a netcat connection
to the destination host and port on the jumpbox.
Running `nc` will take the stdin from the client and forward it to the remote host.
This will "forward" the connection to remote host and connect stdin and stdout.
This is necessary to respond to ssh on remote host (password or host check).
Without doing this, no prompt would be seen (stdout) and you could not send response input (stdin).

## OpenSSH 5.4 to 7.3
The `-w` ssh option was added that serves the role of connecting stdin and stdout from client to remotehost.
This removes the requirement to have `netcat` installed.

## OpenSSH 7.3
OpenSSH 7.3 was 2016-08-01 and introduces `ProxyJump` directive. The command-line options is `-J`.
