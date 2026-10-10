# Skills, and the evidence for each

The rule I apply to suppliers in [evidence-review-engine](https://github.com/karthikbhumireddy/evidence-review-engine) applies here too: **a claim without evidence scores zero.**

How to read this:

- **Evidence** links to something you can open or run. "Self-reported" means my own account of my work history. It is true to the best of my knowledge, but nothing here independently verifies it.
- **Depth** describes what the artefact demonstrates, not years of experience.
- The repositories were built with **Claude Code as an AI pair programmer, directed by me**. I don't list a language or framework just because it appears in generated code or a dependency file. It appears below only where a repo uses it to do something substantive that is tested.

*Last reviewed: October 2026.*

## 1. Professional experience (self-reported)

| Skill | Where | Evidence | Depth | Confidence | What would show more |
|---|---|---|---|---|---|
| Payments product management | Qenta; earlier Paytm, Dineout (restaurant payments) | Self-reported. [payments-reliability-lab](https://github.com/karthikbhumireddy/payments-reliability-lab) shows I understand the failure modes behind payment requirements | Product ownership, not implementation of those employers' systems | Self-reported | A sanitised case study of a shipped payments decision |
| Responsible-sourcing due diligence product | Qenta (Responsible Gold) | Self-reported. [evidence-review-engine](https://github.com/karthikbhumireddy/evidence-review-engine) is a clean-room model of the problem class | Domain modelling: evidence, risk scoring, reviewer workflow | Self-reported | Public writing on due-diligence product design |
| Digital assets and identity products | Qenta (G-Coin, QID) | Self-reported. Product-strategy contribution, not ownership of the underlying technology | Contributor | Self-reported | — |
| Merchant acquisition and go-to-market | Dineout | Self-reported | — | Self-reported | A case study with sourced numbers |
| Entrepreneurship and brand strategy | Deccan Foods (co-founder, brand strategist) | Self-reported | — | Self-reported | — |
| Marketing and entrepreneurship (education) | MBA, Rice Business, 2024 | Self-reported | — | Self-reported | — |

## 2. Technical capabilities demonstrated in code

| Capability | Evidence | Depth shown | Confidence |
|---|---|---|---|
| State machines with enforced transitions | Review workflow ([`workflow.py`](https://github.com/karthikbhumireddy/evidence-review-engine/blob/main/src/evidence_review/workflow.py)), payment states ([`domain.ts`](https://github.com/karthikbhumireddy/payments-reliability-lab/blob/main/src/domain.ts)), Operon approval engine | Illegal transitions rejected and tested. Compare-and-set updates against concurrent writers | High |
| Idempotency and exactly-once processing | Idempotency-Key semantics and webhook dedupe ([payments-reliability-lab](https://github.com/karthikbhumireddy/payments-reliability-lab)), Stripe event marker (Operon) | Replay, 409 in-flight, 422 on body mismatch, rollback-safe dedupe, all tested | High |
| Webhook security | HMAC verification with tolerance, constant-time compare, secret rotation ([`signature.ts`](https://github.com/karthikbhumireddy/payments-reliability-lab/blob/main/src/signature.ts)) | Seven rejection cases tested | High |
| Reconciliation | [`reconcile.ts`](https://github.com/karthikbhumireddy/payments-reliability-lab/blob/main/src/reconcile.ts) | Five exception classes, strict CSV parsing | Medium (single-currency demo data) |
| Explainable rules engines | [`engine.py`](https://github.com/karthikbhumireddy/evidence-review-engine/blob/main/src/evidence_review/engine.py), versioned YAML rulebook | Deterministic, fingerprinted, per-question trace. 100% branch coverage on the engine | High |
| LLM workflows with guardrails | [Extraction pipeline](https://github.com/karthikbhumireddy/evidence-review-engine/blob/main/src/evidence_review/extraction/pipeline.py) and [eval harness](https://github.com/karthikbhumireddy/evidence-review-engine/tree/main/evals) | Schema validation, grounding checks, retry with feedback, refusal routing, cost and latency per attempt | **Medium.** The harness and baseline are real. The live-model evaluation has **not been run yet** |
| Tamper-evident audit logging | Hash-chained log (Python), trigger-enforced append-only table (SQL) | Tampering by edit and by deletion detected in tests | High |
| Automated testing | pytest (59 tests, 98% branch coverage), Vitest (59 tests, 89% branch coverage), Vitest unit tests on Operon (13) | Failure-path heavy. Operon's tests are unit tests against a Prisma fake, not database integration tests | High for logic, low for integration |
| CI and supply-chain hygiene | GitHub Actions workflows: tests, lint, types, gitleaks, link check, Dependabot | Workflows written. Results are visible in each repo's Actions tab once published | Medium until runs are visible |

## 3. Languages and frameworks used substantively

| Technology | Where it does real work | Honest level |
|---|---|---|
| Python (typed, `mypy --strict`) | evidence-review-engine | Working proficiency, AI-assisted |
| TypeScript (strict) | payments-reliability-lab, Operon | Working proficiency, AI-assisted |
| SQL (SQLite schema, constraints, triggers; Postgres via Prisma) | payments-reliability-lab, Operon | Schema design and constraints. No query-performance work shown |
| Next.js App Router, Prisma, Clerk, Stripe | Operon | Prototype level |
| Fastify, Pydantic, Vitest, pytest | as above | Used where tested |

## 4. Actively learning

Postgres concurrency and integration testing, production observability (tracing, metrics), and running LLM evaluations against real traffic.

## 5. Not claimed

I am not claiming expertise in distributed systems, cloud infrastructure, security engineering, machine-learning research or blockchain engineering. My Qenta work touches digital assets and identity as a product role. It is not low-level blockchain development.
