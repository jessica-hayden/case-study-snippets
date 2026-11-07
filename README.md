# Case Study Snippets

Code from a selection of engineering case studies and notes on my portfolio site. Each folder holds a snippet plus a short write-up of the decision behind it.

Most of these are illustrative extracts of a specific pattern or decision, not full production systems. `open-redirect-guard` is a small runnable module with tests. Each README links back to the full write-up, which covers the investigation, the trade-offs, and the outcome in more depth.

## Contents

- **[async-ingestion-pipeline](./async-ingestion-pipeline)**: diagnosing a silent failure caused by a blocking call hidden inside an async task
- **[webhook-validation-layer](./webhook-validation-layer)**: a defense in depth validation layer balancing strict security against high availability
- **[fault-tolerant-data-feed](./fault-tolerant-data-feed)**: an automated pipeline designed to never let bad state replace good state
- **[open-redirect-guard](./open-redirect-guard)**: a post-login redirect guard, with the three versions and the tests that found the gaps in the first two

Full write-ups are on my portfolio site: [jesshayden.netlify.app](https://jesshayden.netlify.app)

## About

Jess Hayden. Automation consultant and systems analyst. Contact: jz.hayden@icloud.com