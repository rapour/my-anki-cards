HSTS (the `Strict-Transport-Security` response header) makes a browser use only HTTPS for a host once it has seen the header. Which visits does that leave unprotected, and how does the **HSTS preload list** close the gap?

---

**The gap: trust on first use.** A browser learns the policy only from an HTTPS response. So it is unprotected:

- on the **very first visit**, whose first request may still be plain HTTP;
- after the stored policy **expires** (`max-age` ran out with no visit);
- after the user **clears browsing data**, or on a **new device** or browser profile.

On those visits, an attacker on the network can still keep the user on plain HTTP (SSL stripping).

**The fix: preloading.** Browsers ship with a built-in list of host names that are HTTPS-only from the start. The list is maintained for Chrome at hstspreload.org and also used by other major browsers. A preloaded domain is protected even on the first visit from a brand-new browser.

To be accepted, a site must, according to hstspreload.org:

1. serve a valid certificate;
2. redirect HTTP to HTTPS on the same host, if it listens on port 80;
3. serve **all subdomains** over HTTPS, including `www` if it has a DNS record, and internal ones that aren't public;
4. send, on the base domain over HTTPS, a header with `max-age` of at least `31536000` (one year), plus `includeSubDomains` and `preload`:

```text
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

**It is hard to undo.** The list is compiled into browsers, so adding or removing a domain only takes effect when users update. hstspreload.org warns that new entries can take several months to reach users, and that removal is slow and painful. Every subdomain, including ones you create later, must work over HTTPS for good.

Whole top-level domains can be preloaded too. Every name under `.dev` and `.app` is HTTPS-only in browsers from the start.
