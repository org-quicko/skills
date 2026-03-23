---
name: tax-qna-thread-research
description: Research skill for Indian tax topics destined for qna.tax threads. Takes a topic as input and produces a verified, source-cited research document — rules, rates, IT Act 2025 provisions, recent amendments, CBDT notifications, examples, and edge cases. Uses web search from credible sources only — ITD, CBDT, taxmann, taxguru, caclubindia. Never uses fintech blogs, news sites, or aggregators. Trigger when the user says "research [tax topic]", "find information about [topic] for the thread", "what are the current rules for [topic]", or asks for research before writing a thread.
---

# Tax Q&A Thread Research

Produce a verified, source-cited research document on any Indian tax topic — ready to hand off to the `tax-qna-thread-writer` skill.

---

## Step 1: Clarify the Scope

Before searching, confirm what you're actually researching:

- **Topic** — What exactly is the subject? If the user's input is vague (e.g., "capital gains"), ask one clarifying question to narrow it down (e.g., which asset class, which taxpayer type). Don't research the wrong angle.
- **Tax Year** — Default to the current Tax Year unless specified otherwise.
- **Taxpayer type** — Resident individual, NRI, company, HUF, partnership? Rules often differ significantly. Infer from context or ask if unclear.

---

## Step 2: Source Rules

Every fact, number, rate, and provision reference must come from an approved source.

**Tier 1 — Statutory / Official (always prefer these)**

| Source | What it covers | URL |
|--------|---------------|-----|
| Income Tax Department portal | Acts, forms, notifications, circulars | https://www.incometax.gov.in |
| CBDT circulars & notifications | Rule changes, clarifications, exemptions | https://incometax.gov.in/iec/foportal/help/rules-regulations-orders-and-circulars |
| India Code | Full text of IT Act 2025 and other central acts | https://www.indiacode.nic.in |
| e-Gazette of India | Gazette notifications, Finance Acts, Rules | https://egazette.nic.in |
| SEBI | Capital markets, mutual fund regulations | https://www.sebi.gov.in |
| RBI | Banking, FEMA, NRI rules | https://www.rbi.org.in |
| MCA | Company law, LLP Act | https://www.mca.gov.in |

**Tier 2 — Credible Professional / Community**

| Source | Why it qualifies |
|--------|-----------------|
| taxmann.com | Specialist tax publisher; editorially rigorous; covers case law and amendments |
| taxguru.in | Practitioner-written; covers circulars, notifications, Budget analysis |
| caclubindia.com | CA community; useful for practical interpretations and compliance discussions |

**Blocked — never use, even if prominently ranked**

- **Fintech/commercial**: ClearTax, Groww, Zerodha Varsity, ET Money, Scripbox — commercially motivated, often simplified or outdated
- **News and media**: Zee News, NDTV, India Today, Economic Times, Times of India, Mint, Business Standard
- **Aggregators**: BankBazaar, PolicyBazaar and similar — built for lead generation, not accuracy
- **Blogs and personal sites**: Any site where editorial process and author credentials are unclear

**The test:** Is this a statutory authority, a specialist tax publisher, or a verified CA community? If not, don't use it.

When a fact only appears on blocked sources, flag it as unverified rather than including it as fact.

---

## Step 3: Research

Search systematically across approved sources. Use targeted `site:` queries:

- `site:incometax.gov.in [topic]`
- `site:taxmann.com [topic]`
- `site:taxguru.in [topic] notification`
- `site:caclubindia.com [topic] [Tax Year]`
- `CBDT circular [topic] 2025`
- `[topic] Finance Act 2025 amendment`

For form-related topics, find the official draft on incometax.gov.in first, then use taxmann for commentary.

Cross-reference across sources — a single taxmann article may have the rate correct but miss a CBDT clarification that creates an exception.

**Before including any number, rate, or provision:**
1. Confirm it in a Tier 1 source where possible; if only in Tier 2, note that
2. Check the effective date — note the Tax Year it applies to; if something changed, document both old and new rules with dates
3. Use IT Act 2025 provision numbering — the 2025 Act renumbered most sections from the old 1961 Act; if a source uses old numbering, find the current equivalent
4. Flag anything unverified: `⚠️ Unverified — could not confirm in approved sources`

---

## Step 4: Output

Present findings as a clean research document. Include all sections that are relevant to the topic — skip what genuinely doesn't apply.

```
# Research: [Topic]

**Tax Year:** [e.g., Tax Year 2025-26]
**Taxpayer type:** [e.g., Resident individuals]
**Date researched:** [today's date]

---

## Core Provision
[Governing section/schedule/rule. Summarise precisely. Include IT Act 2025 reference
and old 1961 Act reference if useful for continuity.]

Provision: [e.g., Section X, IT Act 2025 (previously Section Y, IT Act 1961)]
Source: [URL]

---

## Key Numbers
[Every rate, threshold, limit, and date the thread will need.]

| Item | Value | Applicable from | Source |
|------|-------|----------------|--------|
| ... | ... | ... | [URL] |

---

## Recent Changes
[What changed in the last 1–2 Tax Years — Budget amendments, Finance Act, CBDT notifications.]

| What changed | Old rule | New rule | Effective from | Source |
|-------------|----------|----------|---------------|--------|
| ... | ... | ... | ... | [URL] |

[If nothing changed: "No significant changes in Tax Year 2024-25 or 2025-26."]

---

## Procedure / Compliance Steps
[What the taxpayer actually has to do — form, portal, deadlines, TAN/PAN, challan.]

1. [Step]
2. ...

Due dates:
| Action | Due date |
|--------|---------|
| ... | ... |
Source: [URL]

---

## Exemptions and Exceptions
- [Exception — with source URL]

---

## Edge Cases and Common Questions
[The non-obvious questions forum readers come specifically to find.]

Q: [Question]
A: [Specific, sourced answer]

---

## Worked Example
[Concrete example with real ₹ amounts. Full calculation where applicable.]

Scenario: [...]
Calculation:
- [Step]
- [Result]

---

## Case Law / CBDT Clarifications
[Tribunal decisions, HC rulings, AAR rulings, CBDT circulars on contested interpretations.
Skip if none found.]

| Case / Circular | Ruling / Clarification | Source |
|----------------|----------------------|--------|
| ... | ... | [URL] |

---

## Related Provisions and Cross-References
- [Provision/Form — why it's relevant]
- [Related qna.tax thread URL if known]

---

## Unverified / Flagged Items
- ⚠️ [Item] — found only on [source], could not confirm in approved sources
[If nothing: "All key facts verified in approved sources."]

---

## Sources

Tier 1 — Statutory / Official
- [Name] — [URL]

Tier 2 — Professional / Community
- [Name] — [URL]
```

---

## Handoff

After presenting the document, tell the user:

> "Ready to pass to the `tax-qna-thread-writer` skill. Share this as-is or add your own opinions and angles before handing it over."