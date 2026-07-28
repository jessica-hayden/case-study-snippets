"""
Illustrative snippet from the "Fault Tolerant Data Feed" case study.
Not the full production implementation, see the README in this folder
for context on the problem and the decision behind this approach.
"""

import hashlib


def validate_and_apply_rules(raw_payload: bytes, expected_hash: str, active_rule_count: int):
    # Stage 1: Verify payload integrity via SHA-256 digest
    computed_hash = hashlib.sha256(raw_payload).hexdigest()
    if computed_hash.lower() != expected_hash.lower():
        raise ValueError("Payload integrity error: SHA-256 mismatch.")

    # Stage 2: Parse items and check volume stability threshold
    parsed_rules = [line.strip() for line in raw_payload.decode("utf-8").splitlines() if line]

    # Abort if incoming list unexpectedly drops significantly compared to active set
    if len(parsed_rules) < (active_rule_count * 0.70):
        raise RuntimeError(
            f"Safety check triggered: incoming rule count ({len(parsed_rules)}) "
            f"dropped significantly compared to active rules ({active_rule_count}). Aborting."
        )

    # Atomic deployment to active firewall engine
    return apply_firewall_rules(parsed_rules)
