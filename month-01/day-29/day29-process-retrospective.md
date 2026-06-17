# Day 29 — How I Actually Work: A Process Retrospective

**Date:** 2026-06-11

---

## Why I'm Writing This

Day 28 was about what I know — skills, gaps, job requirements. This one is different. This is about how I actually work when I'm investigating something, not what tools I've touched. Anyone can list YARA and Sigma on a CV. Fewer people can explain how they think when they hit a wall, and that's the part that actually matters in a real SOC seat.

---

## What I Do When I Get Stuck

My first move is to sit with the problem and try things myself before reaching for help. Not because asking for help is wrong, but because the struggle is where the actual learning happens. If I jump straight to an answer the first time something doesn't make sense, I never build the instinct for next time. I'd just be collecting answers, not understanding investigations.

That said, I do use Claude — but as a guide, not an answer machine. I ask it to point me toward where to look (which Event ID, which filter, which tool) rather than asking it to tell me what the finding is. There's a real difference between "what's the answer" and "where should I be looking." The second one keeps me doing the actual work.

I noticed this clearly during the BTLO phishing investigation. I could have asked for every answer directly. Instead I worked through the headers myself, decoded the base64 myself, and only asked for confirmation when I was stuck on the exact URL format BTLO wanted. That's the difference between doing the investigation and watching someone else do it.

---

## How I Verify a Finding

I re-read the evidence slowly before trusting what I think I found. Not a second tool, not a cross-check with another source — just going back through the actual logs or headers again, more carefully the second time.

This is something I want to get better at. Re-reading catches mistakes I made from rushing, but it doesn't catch mistakes in my understanding. If I misread a registry path the first time, reading it slowly a second time doesn't fix that — I'd need a second method or a second source to actually validate it. Right now my verification process is single-threaded. That's a gap I should close in Month 2 — start cross-referencing findings against a second tool or source before calling something confirmed.

---

## What's Actually Been Hard

Two things, and they're connected.

**Time management around school.** I'm a full time CS student running this roadmap on top of coursework. Some days the roadmap gets the leftover hours after everything else is done, which means the depth of my work varies day to day depending on how much school took out of me.

**Not knowing if it's actually working.** This is the harder one. There's no scoreboard for "is this making me hireable." I can complete a challenge and get 10/10 and still not know if that translates to anything real. Twenty-nine days of consistent work and I still don't have external confirmation that any of it matters yet — no interview, no recruiter message, no signal from outside my own head that says "yes, this is working." I'm operating on faith that consistency compounds, without proof yet that it does.

---

## What I'm Doing About Both

For time management — I'm not trying to fix this by working harder. I'm fixing it by making each day's documentation tighter so the same hours produce more usable output. A focused 90 minutes that produces a real artifact beats 3 scattered hours that produce nothing I can point to later.

For the uncertainty — I think the honest answer is I won't know if it's working until it works. The GitHub commits, the LinkedIn posts, the connection requests to SOC managers — none of that has a guaranteed payoff. What I can control is whether the work is real and well documented. Day 28's skills matrix gave me a concrete next step instead of vague anxiety. That's the antidote to "is this working" — turning the uncertainty into a checklist instead of a feeling.

---

## What I Concluded

The technical skills are coming along. The process skills — how I verify things, how I manage limited time, how I sit with not knowing — are just as important and get talked about less. Nobody puts "tolerates uncertainty" on a CV but it's probably the actual skill keeping me consistent through 29 days when there's no proof yet that any of it is working.

---

## One Thing I Want to Change Starting Month 2

Stop verifying findings with a single re-read. Start cross-checking every conclusion against at least one other method or source before I call it confirmed. Re-reading catches carelessness. It doesn't catch wrong assumptions. I need a second check, not a second look.
