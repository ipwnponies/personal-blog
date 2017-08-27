---
layout: default
title: SSH Tunneling
---
# SSH Tunnel Forwarding

## Motivation
What's the purpose of ssh tunnels?
They let us proxy traffic through the tunnel, creating a worm hole of sorts.
From the ssh client perspective, there is a port feeds right into another network.

## Local Port Forwarding
```
ssh -L 1337:localhost:80 user@remotehost
```
This will advertise `remotehost:80` to the local network via `localhost:1337`.
Users in the local network can access the remote service by connecting to `localhost`
without needing to access remote network.

Use local port forwarding when you need to access remote services but are not able to access,
you can use the host that is able to connect to serve as a proxy.

## Remote Port Forwarding
```
ssh -R 80:localhost:1337 user@remotehost
```
This will advertise `localhost:80` to the remote network via `remotehost:1337`.
Users in the remote network can access the local service by connecting to `remotehost`
without needing access to local network.

Use remote port forwarding when you want to advertise a local service into a remote network.

## Dynamic Port Forwarding
```
ssh -D 1337 user@remotehost
```
This is similar, in intent, to local port forwarding.
This command will configure port 1337 on local host to forward into the remote network.
This is how you set up a SOCKS proxy, tunneling all web traffic from a web browser to the remote network.
This can be used to access intranet resources when we aren't actually on the network.
It can also be used to access resources that have been blocked, such as facebook or gmail.
Instead of TCP traffic going out to facebook.com, the traffic would be sent to the ssh tunnel instead.
It would look like ssh data going to `remotehost.
