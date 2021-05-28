---
title: HTTP Cookies Are A Mess
categories: programming
tags:
  - web
  - technology
---

Wow, are HTTP cookies are mess.
I've had the displeasure of learning this and discovering how web browsers have been bolting and duct taping this system
together.

## What Are Http Cookies

The web, and HTTP protocol, was designed to be stateless.
The modern web doesn't like to be stateless.
Websites want to save preferences or track users.

To achieve state, early browsers allowed cookies to be stored and sent to the server.
The idea was that you stored an INI config and sent it up with every HTTP request.

Over time, this has morphed into storing a session cookie and sending that session cookie back to the server.
The server can then use this session cookie/key to retrieve the server-side session data or user profile.

## Namespacing and Scope

Cookies are keyed on name, domain, and path.

Web hosting services often provide users with subdomains, _foo.example.com_ and _bar.example.com_.
You wouldn't want the cookies to be sent across domains.

Or maybe you have a subpath on a shared web server, such as university web server.
You can set cookies and key by path, so that the cookie is only send when accessing your subpath.

In practice though, most sites are configured to a cookie on the top-level domain, which will ensure it's sent to every
request to a subdomain.
This is typically a session cookie, which is a simple unique idenitifier to key on.
This simplifies management, as it's entirely controlled by the backend application.

### Collision

But this "feature" means it's possible to set multiple cookies with the same name, if they don't share domains or paths.
Every cookie that qualifies will be sent up by the browser.
The RFC doesn't dictate what the server will do, just that the [browser will send up][1].

[1]: https://stackoverflow.com/questions/1062963/how-do-browser-cookie-domains-work

Due to market forces, the major browser (Chrome) kind of dictates ordering in practice, and other browser fall in line.
No niche browser is going to lose market share over technical correctness and strict adherence to a spec.
And even worse, the domain and path information is dropped in the request header.
It's entirely ambiguous to the server which cookie belongs to which path or domain.
Conceptually, the backend should be agnostic and trust that the browser sent each cookie because they qualified, based
on this domain and path.

It's entirely [server implementation][2] for how to handle multiple cookies.
In Flask, the design is to resolve to one cookie.
This resulted in a [change of behaviour][3], from "first-in" to "last-in".

[2]: https://stackoverflow.com/a/24214538
[3]: https://github.com/pallets/werkzeug/pull/1458

To summarize this hot mess situation:

- Browser allows setting multiple cookies with same name. The key is `(name, domain, path)`.
- Browser attaches **only** the cookie values to request header, in the arbitrary order it chooses.
  - If multiple cookies share a common name, this is ambiguous cookie value. i.e. `foo=value1;foo=value2`
- Server decides how it should consume multiple cookie values.

### Set-Cookie vs. document.cookie

Cookies are set via the [`Set-Cookie` response header][set-cookie header].
The response header is crafted by the web server.
Whatever the domain is, is set by Chrome.

You can also set cookies via javascript, on client side, using [`document.cookie`][document cookie].
Chrome will add a leading dot prefix to the domain, which also allows for all subdomains.

[set-cookie header]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
[document cookie]: https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie

This means you cannot set a cookie, via javascript, with a domain exactly the same as the cookie received from server.
It will also be another cookie with a different domain, and now you're at the whim of the the multiple cookie [collision](#collision).
Why would you mix and match backend and frontend ways of setting cookies?

Because I was setting a [Cypress] test environment.
And I thought it would be straightforward to set up the browser instance manually, instead of configuring a custom test backend.

[cypress]: https://docs.cypress.io/api/commands/setcookie

### Conclusion

My takeaway here is that you should not use multiple cookies with the same name.
The fact that it's so broken and not well supported across the web means it's probably very uncommon use case.
It's an unwanted feature that has exposed ways to break it.

There's too much "up to implementation" of both web server and browser for this to be stable.
Stay far away from it, find some other workaround.
Fun fact, I ended up monkey-patching `Flask` server handling behaviour, as a last resort...

## Same-Site

`SameSite` is a [`Set-Cookie` attribute][set-cookie header] that lets the server declare if the cookie should be
restricted to first-party context.

[samesite]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite

That's a lot of unpack.
Let's first discuss context.

### Context

First-party context is when you are on _example.com/foo_ and click on a link going to _example.com/bar_.
The browser understands this to be first-party and controlled by the same entity.

Third-party context is a little trickier.
Loading images or frames from a differnt site is a cross-site request.
Navigating a link to a different site is also a cross-site request.

You can see why third-party context is loaded.
You'd probably want to send cookies when you navigate from _google.com_ search result to _stackoverflow.com_, so that
you're logged in.
But what about embedded stackoverflow posts, while you're on _google.com_ search result?

### Strict, Lax, None

`SameSite` comes in 3 flavours: `Strict`, `Lax`, `None`.

`Strict` is first-party context only.
This is very safe, as your cookie is only sent to the site you're on.
The surface vector for CSRF attacks is reduced to nil and you can worry less about it.
The cookie's scope and lifetime is for as long as you travel within the site, link to link.

`Lax` is third-party context but only for navigation.
Google search results is a great example.
You can see why many sites will use this value, you want to recognize users coming in from SEO.

`None` is everything.
The cookie is sent with every request.
This is how the web used to work, it's a naive solution.
This puts you at risk of CSRF attacks.
An attacker can embed your site in an _iframe_ and this redirects visitors and attaches cookies.
The attacker controls the top-level frame and can do lots of things, including run javascript or make requests that
masquerade as your actions.

### Current State

Browsers are moving towards changing the default `SameSite` from `None` to `Lax`.
This reduces permissions and, therefore, break many site that rely on `None` behaviour.
As such, it's taken chrome 2 years to slowly roll this out and convince websites to update their code.

Even though it's been turned on for months now, there are still exceptions.
The ["Lax+POST" exception][lax+post] exists to grant `None` behaviour but only for newly set cookies (2 minutes).
Why?
Many Identity Providers need access to set the cookie on behalf of a different domain, after authenticating the user.
I guess they haven't gotten their shit together because this is only a temporary mitigation, will be removed later.
It's not very well documented and this dynamic time-based expiration is very unexpected.

[lax+post]: https://www.chromestatus.com/feature/5088147346030592
