# Open Redirect Guard: Validate the Output, Not Just the Input

A small, runnable example from the Engineering notes write-up. It is an illustrative module, not production source.

## The problem

After login, an app sends the user back to wherever they were going, passed in a `next` URL parameter. That value is controlled by whoever built the link, so a naive version can be used to send a freshly authenticated user to a malicious site.

## The decision

A guard that validates the input is not the same as one that validates the output. The origin check proves a URL resolves to your own site. It does not prove that the string you then hand back is safe to use.

## Version history

1. **Shape check only.** The value must start with a single slash, and not `//` or `/\`. This misses tab and newline characters, which browsers strip when they parse a URL, so a slash, a tab, then `/evil.com` becomes `//evil.com`.
2. **Added an origin check with `new URL()`.** This closes the tab and newline case. It misses dot segments: `/.//evil.com` resolves to the right origin, then normalises to a pathname of `//evil.com`, which a caller can read as protocol-relative.
3. **Checks the value actually returned.** This is `safe-next.js`.

The test file keeps version two so the gap stays reproducible.

## Running it

Needs Node 18 or later. There are no dependencies.

```
npm test
```

## If I were extending this

- Prefer an allow-list of known routes where the app has a small, fixed set, instead of accepting any same-site path
- Log rejected values, so repeated probing shows up as a signal
- Return route names rather than raw paths where possible

## What I'd do differently

Start from the output. Decide what a safe return value looks like, test that, and work backwards. Write the list of bypass inputs first and treat it as the specification.

Full write-up: [Engineering notes](https://jesshayden.netlify.app/freelance/engineering-notes), part 3.
