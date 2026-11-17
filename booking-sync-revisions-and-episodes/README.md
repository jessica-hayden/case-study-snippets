# Booking Sync: Revisions and Episodes

A small, runnable example from the "Booking sync assurance" write-up. It is an illustrative module, not production source. The product itself was designed as a typed TypeScript contract and then parked.

## The problem

A connector that moves bookings between two systems has to answer two questions correctly. When has a booking really changed, so it must be delivered again? And when is a booking "new" in a way a person cares about, given that one course of treatment is several separate bookings?

## The decision

**Revisions, not fingerprints, as delivery keys.** A content hash is good at detecting change. It is a poor key for delivery. A booking moved from 10:00 to 11:00 and back to 10:00 ends with the same hash it started with, so a hash-keyed system sees nothing new and skips the second move. Giving each accepted change its own revision number makes those three states three deliveries.

**Episodes.** Bookings are grouped per client, service and kind, with a configurable gap. A course of six sessions is one episode, so "course start" fires once. A repeat course after the gap is a new episode. The grouping is recomputed from the full history in start-time order, so live processing, backfill and repair all give the same answer.

## Running it

Needs Python 3.10 or later. There are no dependencies.

```
python3 revisions_and_episodes.py
```

It checks its own examples and prints `ok`.

## If I were extending this

- Persist the head (revision and fingerprint) in the same transaction as the delivery job
- Make the gap per service and kind a setting, which the example already allows
- Add cancelled bookings to the history so an episode can reopen

## What I'd do differently

The first version of the design keyed delivery on content. A review found that a booking moved and moved back would be silently skipped. I would write that case as the first test, before any code.

Full write-up: [Booking sync assurance](https://jesshayden.netlify.app/freelance/booking-sync-assurance)
