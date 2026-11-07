import { test } from 'node:test';
import assert from 'node:assert/strict';
import { safeNext } from './safe-next.js';

const ORIGIN = 'https://portal.example.com';
const FALLBACK = '/review';

// Version 2 of the guard: shape check plus origin check, but no check on the returned value.
// Kept here so the gap it had stays reproducible.
function safeNextVersionTwo(raw, origin) {
  if (typeof raw !== 'string' || !/^\/(?![/\\])/.test(raw)) return FALLBACK;
  try {
    const url = new URL(raw, origin);
    if (url.origin !== origin) return FALLBACK;
    return url.pathname + url.search + url.hash;
  } catch {
    return FALLBACK;
  }
}

const legitimatePaths = [
  ['/history', '/history'],
  ['/history?tab=2#top', '/history?tab=2#top'],
  ['/review', '/review'],
  ['/a/b/c', '/a/b/c'],
];

const bypasses = [
  '//evil.com',
  '/\\evil.com',
  '/\\/evil.com',
  '/.//evil.com',
  '/%2e//evil.com',
  '/a/..//evil.com',
  '/a/%2e%2e//evil.com',
  'https://evil.com',
  'javascript:alert(1)',
  '/\t/evil.com',
  '/\n/evil.com',
  '/\r/evil.com',
  ' //evil.com',
  '',
];

const dotSegmentBypasses = [
  '/.//evil.com',
  '/%2e//evil.com',
  '/a/..//evil.com',
  '/a/%2e%2e//evil.com',
];

for (const [input, expected] of legitimatePaths) {
  test(`allows ${JSON.stringify(input)}`, () => {
    assert.equal(safeNext(input, ORIGIN), expected);
  });
}

for (const input of bypasses) {
  test(`rejects ${JSON.stringify(input)}`, () => {
    assert.equal(safeNext(input, ORIGIN), FALLBACK);
  });
}

for (const input of [null, undefined, 42, {}, []]) {
  test(`rejects non-string input ${JSON.stringify(input)}`, () => {
    assert.equal(safeNext(input, ORIGIN), FALLBACK);
  });
}

test('falls back safely when no origin is available', () => {
  assert.equal(safeNext('/history'), FALLBACK);
});

// Why the final check exists: without it, dot segments normalise to a leading "//"
for (const input of dotSegmentBypasses) {
  test(`version two returned a protocol-relative path for ${JSON.stringify(input)}`, () => {
    assert.ok(safeNextVersionTwo(input, ORIGIN).startsWith('//'));
  });
}
