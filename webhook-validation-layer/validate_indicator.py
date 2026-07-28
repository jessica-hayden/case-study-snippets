"""
Illustrative snippet from the "Webhook Validation Layer" case study.
Not the full production implementation, see the README in this folder
for context on the problem and the decision behind this approach.
"""

import unicodedata
import ipaddress
from pydantic import BaseModel, validator, Field


class IncomingReportModel(BaseModel):
    indicator: str = Field(..., max_length=253)
    description: str = Field(..., max_length=5000)

    @validator("indicator", pre=True)
    def normalise_and_validate_indicator(cls, value: str) -> str:
        # Step 1: Prevent Unicode bypass techniques
        normalised = unicodedata.normalize("NFKC", str(value)).strip()

        # Step 2: Deterministic IP check (prevents ReDoS backtracking)
        try:
            ipaddress.ip_address(normalised)
            return normalised
        except ValueError:
            pass

        # Fallback length/format check
        if len(normalised) > 253 or " " in normalised:
            raise ValueError("Malformed indicator string")

        return normalised
