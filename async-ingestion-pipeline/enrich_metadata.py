"""
Illustrative snippet from the "Async Ingestion Pipeline" case study.
Not the full production implementation, see the README in this folder
for context on the problem and the decision behind this approach.
"""

import logging

logger = logging.getLogger(__name__)


async def enrich_metadata(identifier: str, client) -> dict:
    """Non-blocking lookup with bounded timeout and fallback."""
    try:
        response = await client.get(f"/lookup/{identifier}", timeout=0.5)
        response.raise_for_status()
        return response.json()
    except (TimeoutError, HTTPError) as err:
        logger.warning(f"Enrichment failed for {identifier}: {err}")
        return {"id": identifier, "enriched": False, "fallback_mode": True}
