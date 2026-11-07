/**
 * Returns a same-site path that is safe to redirect to after login.
 * Anything that is not a clean same-site path falls back to a default route.
 *
 * Illustrative snippet from the "Engineering notes" write-up, not production source.
 */

const FALLBACK = '/review';

export function safeNext(raw, origin = globalThis.window?.location.origin) {
  // 1. Shape check: a string that starts with a single "/", not "//" or "/\"
  if (typeof raw !== 'string' || !/^\/(?![/\\])/.test(raw)) return FALLBACK;

  try {
    // 2. Ask the URL parser where this really leads, instead of guessing from the string
    const url = new URL(raw, origin);
    if (url.origin !== origin) return FALLBACK;

    // 3. Check the value we actually return, not just the parse.
    //    Dot segments can normalise to a leading "//", which a caller may read as off-site.
    const out = url.pathname + url.search + url.hash;
    if (!out.startsWith('/') || out.startsWith('//') || out.startsWith('/\\')) return FALLBACK;

    return out;
  } catch {
    return FALLBACK;
  }
}
