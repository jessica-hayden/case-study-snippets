# Fault Tolerant Data Feed: Never Let Bad State Replace Good State

This is an illustrative snippet extracted from a larger system, not the full implementation.

## The problem

An hourly automated job pulled third party threat intelligence data to update production firewall rules with no human in the loop. External vendor APIs fail in unpredictable ways: rate limits, dropped connections, partial payloads. In this context, an incomplete or corrupted transfer overwriting the active configuration is serious, most active rules would simply disappear.

## The decision

Never allow bad state to replace good state. If a download fails an integrity check or the incoming rule count drops sharply compared to the active set, the job aborts, raises an alert, and leaves the existing rules untouched. A stale ruleset for an extra hour is far preferable to an empty or corrupted one applied instantly.

## The code

`validate_and_apply_rules.py` runs two checks before any deployment: a cryptographic hash check against the vendor's expected digest, and a volume stability check against the currently active rule count. Either failing aborts the deploy entirely.

## If I were extending this

I'd add a dry-run mode that logs what the deployment would have changed without actually applying it, useful for catching a vendor's gradual, legitimate list changes before they ever approach the abort threshold.

## What I'd do differently

The 30% volume threshold was chosen empirically, if I were setting this up again I'd want a rolling baseline built from several weeks of vendor data rather than a single fixed percentage, since some vendors naturally fluctuate more than others.

Full case study: [link once live]
