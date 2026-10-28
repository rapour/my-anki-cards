You want to turn on HSTS (the `Strict-Transport-Security` header, which makes browsers use only HTTPS for your host) for a production site. What can go wrong, and how do you roll it out safely?

---

**What can go wrong:**

- **Browsers remember it.** For `max-age` seconds, users who saw the header can't reach the host over plain HTTP. A subdomain or page that only works over HTTP is broken for them, and you can't fix it from the server until the policy expires.
- **`includeSubDomains` reaches everything below,** including internal names such as `printer.office.example.com` or a test server with a self-signed certificate. HSTS also turns any certificate error on those hosts into a hard failure, with no "proceed anyway".
- **It doesn't redirect anyone.** Browsers ignore the header over plain HTTP, so a first-time visitor still needs a normal HTTP-to-HTTPS redirect on port 80.
- **It only binds browsers.** Scripts and API clients generally ignore it (curl only uses it when given a cache file with `--hsts`).

**Safe rollout**, as hstspreload.org recommends:

1. Check that every subdomain, public and internal, works over HTTPS.
2. Send the header on all HTTPS responses, raising `max-age` in stages:
   - `max-age=300; includeSubDomains`: 5 minutes;
   - `max-age=604800; includeSubDomains`: 1 week;
   - `max-age=2592000; includeSubDomains`: 1 month.
3. At each stage, watch for broken pages and traffic drops, fix them, and wait out the full `max-age` before the next stage. A mistake at 5 minutes heals in 5 minutes; a mistake at one year lasts a year.
4. Then go to `max-age=31536000` (one year) or more. Add `preload` only if you want to join the browsers' built-in list, which is much harder to leave.

**Undoing it.** Serve `Strict-Transport-Security: max-age=0` **over HTTPS**. Each browser drops the policy the next time it receives that response. A browser that never comes back keeps the old policy until its `max-age` runs out.
