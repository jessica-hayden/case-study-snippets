# Async Ingestion Pipeline: Non-Blocking Enrichment with Fallback

This is an illustrative snippet extracted from a larger system, not the full implementation.

## The problem

A high throughput ingestion service looked healthy on every standard dashboard while silently dropping data under load. The root cause was a synchronous network call sitting inside an async task, quietly blocking the event loop without ever raising an error.

## The decision

Degrade gracefully rather than fail closed. A missing piece of enrichment metadata is a smaller problem than a missing record entirely, so the fallback path persists the core data with a flag rather than dropping it.

## The code

`enrich_metadata.py` rewrites the enrichment call as non-blocking, with a bounded timeout and a fallback that keeps the pipeline moving if the dependency is slow or unavailable.

## If I were extending this

I'd add a circuit breaker around the enrichment call so that after a run of consecutive failures, the pipeline stops attempting enrichment for a short cooldown window rather than retrying a dependency that's clearly down. Right now every call pays the same timeout cost even when the dependency has already failed several times in a row.

## What I'd do differently

In hindsight, a 0.5 second timeout was a reasonable starting point, but I'd want real latency data from the dependency before fixing that number. A fixed timeout is a guess until it's backed by actual percentile data from production traffic.

Full case study: [link once live]
