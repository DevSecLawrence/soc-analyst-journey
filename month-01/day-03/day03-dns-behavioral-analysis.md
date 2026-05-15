## What I Concluded
DNS is more than name lookups. In this capture, I could see both browser activity and background system activity just from the queries.

The traffic split pretty cleanly into two groups:
- System-generated activity: certificate checks and background service lookups like `contile.services.mozilla.com`, `o.pki.goog`, `ocsp.starfieldtech.com`, `ocsp.sectigo.com`, `firefox.settings.services.mozilla.com`, and `content-signature-2.cdn.mozilla.net`
- Browser-generated activity: sites and assets tied to browsing like `www.google.com`, `github.com`, `github.githubassets.com`, `avatars.githubusercontent.com`, `fonts.gstatic.com`, `csp.withgoogle.com`, `wikipedia.org`, and `lh3.googleusercontent.com`

The main thing I learned is that DNS shows more than just destination IPs. It shows what the machine is trying to do. A lot of the traffic here was background trust checks, content delivery lookups, and service validation, not just the sites I meant to open.

I also wrote a small Python script to tag the CSV into `browser`, `system`, and `unknown`. That helped a lot for triage, but I still checked the output by hand because the labels only make sense if the rules are sane. In this capture, the final CSV ended with zero unknowns, which was okay because the remaining domains still had a clear explanation.

## Assumption I Made
I assumed that if a DNS query showed up while I was browsing, it was either something I asked for or some background dependency of the browser or OS.

That was not really true. A lot of what looked like simple browsing was actually certificate checks, service endpoints, CDN assets, and other background lookups. So the session was bigger than the sites I clicked on.

## Uncertainty I Have
I still do not have a perfect line between browser-generated background behavior and system-generated behavior for every domain family.

For example, some Google and Mozilla queries are clearly support traffic, but they still feel more like browser activity than pure OS activity. Next I want to do the hard exercise and compare these normal queries to suspicious domains so I can look at entropy, naming patterns, and response behavior.
