# Webhook Validation Layer: Deterministic Parsing Over Regex

This is an illustrative snippet extracted from a larger system, not the full implementation.

## The problem

A multi tenant ingestion platform needed to reject genuine security threats without dropping legitimate vendor data over minor formatting noise. The existing validation relied heavily on complex regular expressions, which fuzz testing showed were vulnerable to catastrophic backtracking, a single crafted long string could freeze the validation layer entirely.

## The decision

Replace pattern matching with deterministic standard library parsing wherever possible, and split validation into a clear reject-versus-sanitise policy rather than a binary pass or fail rule. Hard failing every payload with trailing whitespace or casing quirks shifts the burden onto upstream partners; sanitising acceptable noise while strictly blocking structural threats preserves both security and reliability.

## The code

`validate_indicator.py` normalises input with Unicode NFKC normalisation to prevent bypass techniques, then checks structure using `ipaddress.ip_address` rather than a regex pattern, removing the backtracking risk entirely.

## If I were extending this

I'd add a metrics counter tracking how often the sanitise path fires per vendor, so a sudden spike in a specific vendor's formatting noise would surface as a signal worth investigating, rather than silently absorbing it forever.

## Related patterns

The same underlying principle, fail safe rather than fail total, shows up again in the fault-tolerant data feed snippet in this repo, just applied to a very different kind of system.

Full case study: https://jesshayden.netlify.app/analyst/validation-layer-webhook-ingestion
