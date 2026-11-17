"""
Booking sync assurance: two core ideas, illustrated.

1. A content fingerprint detects change, but each accepted change gets its own
   revision number. Delivery is keyed on the revision, so a booking moved from
   10:00 to 11:00 and back to 10:00 is delivered three times, not skipped.
2. Bookings are grouped into episodes per client, service and kind, so a course
   of six sessions is one "course start", and a repeat course after a gap is a
   new one.

Illustrative only; the production design is a typed TypeScript contract.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta

VOLATILE = {"source_updated_at"}


def fingerprint(booking: dict) -> str:
    stable = {k: v for k, v in booking.items() if k not in VOLATILE}
    return hashlib.sha256(json.dumps(stable, sort_keys=True).encode()).hexdigest()


@dataclass
class Head:
    revision: int
    fingerprint: str


def accept(head: Head | None, booking: dict) -> Head | None:
    """Return the new head if this observation is a real change, else None."""
    fp = fingerprint(booking)
    if head is None:
        return Head(1, fp)
    if fp == head.fingerprint:
        return None  # identical resend: no new revision
    return Head(head.revision + 1, fp)


def delivery_key(destination: str, booking_id: str, head: Head) -> str:
    return f"{destination}:{booking_id}:r{head.revision}"


@dataclass
class Episode:
    key: str
    booking_ids: list[str] = field(default_factory=list)


def assign_episodes(bookings: list[dict], gap_days: dict[str, int], default_gap: int = 180) -> list[Episode]:
    """Group active bookings into episodes, independent of arrival order."""
    active = [b for b in bookings if b["status"] in ("booked", "arrived")]
    active.sort(key=lambda b: (b["starts_at"], b["id"]))
    episodes: list[Episode] = []
    last_start: dict[str, datetime] = {}
    current: dict[str, Episode] = {}
    for b in active:
        group = f'{b["client"]}:{b["service"]}:{b["kind"]}'
        gap = timedelta(days=gap_days.get(f'{b["service"]}:{b["kind"]}', default_gap))
        start = datetime.fromisoformat(b["starts_at"])
        if group not in current or start - last_start[group] > gap:
            current[group] = Episode(group)
            episodes.append(current[group])
        current[group].booking_ids.append(b["id"])
        last_start[group] = start
    return episodes


if __name__ == "__main__":
    h1 = accept(None, {"id": "b1", "starts_at": "10:00"})
    h2 = accept(h1, {"id": "b1", "starts_at": "11:00"})
    h3 = accept(h2, {"id": "b1", "starts_at": "10:00"})
    assert h1 and h2 and h3 and h1.fingerprint == h3.fingerprint
    assert delivery_key("crm", "b1", h1) != delivery_key("crm", "b1", h3)

    course = [{"id": f"t{i}", "client": "c1", "service": "course", "kind": "treatment",
               "status": "arrived", "starts_at": f"2026-09-{10 + i * 3:02d}T10:00:00"} for i in range(6)]
    repeat = course + [{"id": "t9", "client": "c1", "service": "course", "kind": "treatment",
                        "status": "booked", "starts_at": "2027-02-01T10:00:00"}]
    assert len(assign_episodes(repeat, {"course:treatment": 60})) == 2
    print("ok")
