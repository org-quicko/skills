# Google Search Console (GSC) Integration

Google Search Console is Google's official tool for monitoring and troubleshooting a site's presence in Google Search results. It's the most authoritative data source for understanding how Google sees your site.

---

## When to Use GSC in the SEO/GEO Workflow

- **Step 2 (Technical Audit):** Pull real crawl errors, indexing status, and Core Web Vitals from GSC instead of guessing
- **Step 3 (Keyword Research):** Use GSC's Performance data to find real search queries your pages already rank for — then optimize for them
- **Step 6 (Validate & Monitor):** Submit sitemaps, request indexing, and track results over time

---

## Accessing Google Search Console

### Via Browser (Claude in Chrome)
```bash
open "https://search.google.com/search-console"
```

Navigate to the relevant property. If the user hasn't verified their site, they'll need to do so first (DNS record, HTML tag, or Google Analytics method).

### Via API (Programmatic Access)

The GSC API requires OAuth2 authentication. Use the scripts in `scripts/gsc_*.py` after setting up credentials.

**Setup:**
```bash
# Install dependencies
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Place your OAuth2 credentials file
# Download from Google Cloud Console > APIs & Services > Credentials
export GSC_CREDENTIALS_FILE=/path/to/credentials.json
export GSC_SITE_URL=https://example.com/  # Must match exact property URL in GSC
```

---

## Key GSC Reports and What to Do With Them

### 1. Performance Report
**Location:** Search Console > Performance > Search results

**What it shows:** Clicks, impressions, CTR, average position for queries and pages over time.

**How to use it in the SEO workflow:**
- Export queries with high impressions but low CTR → these pages need better meta titles/descriptions
- Export queries ranked in positions 5-20 → these are "quick win" optimization targets
- Compare page-level performance to identify which pages drive traffic vs. which are invisible

**API Query:**
```python
# See scripts/gsc_performance.py
# Gets top queries, pages, countries, devices for a date range
python3 scripts/gsc_performance.py --site https://example.com/ --days 90 --dimension query
python3 scripts/gsc_performance.py --site https://example.com/ --days 90 --dimension page
```

**Key Metrics:**
| Metric | What It Means | Action Trigger |
|--------|--------------|----------------|
| CTR < 2% with > 1000 impressions | Title/description not compelling | Rewrite meta tags |
| Position 5–20 | Close to page 1, worth optimizing | Update content, add schema |
| Position 1–3, low impressions | Keyword has low volume or wrong intent | Find better keywords |
| Impressions dropping | Ranking loss or crawl issue | Check Index Coverage |

---

### 2. Index Coverage Report
**Location:** Search Console > Indexing > Pages

**What it shows:** Which pages are indexed, excluded, and why.

**Status meanings:**
- **Valid** — Page is indexed ✅
- **Valid with warning** — Indexed but has issues (duplicate content, etc.)
- **Error** — Not indexed due to a problem ❌
- **Excluded** — Not indexed intentionally or by choice (noindex, duplicate, etc.)

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| Server error (5xx) | Server instability | Fix server, resubmit URL |
| Redirect error | Broken redirect chain | Fix redirect, resubmit |
| Submitted URL not found (404) | Page deleted but still in sitemap | Remove from sitemap or restore page |
| Crawled - currently not indexed | Google crawled but chose not to index | Improve content quality, add internal links |
| Duplicate without canonical | Duplicate pages, no canonical tag | Add `<link rel="canonical">` |
| Blocked by robots.txt | robots.txt is blocking Googlebot | Fix robots.txt rules |
| noindex tag | Page has `<meta name="robots" content="noindex">` | Remove noindex if page should be indexed |

**API Query:**
```python
python3 scripts/gsc_index_coverage.py --site https://example.com/
```

---

### 3. Sitemaps
**Location:** Search Console > Indexing > Sitemaps

**What to do:**
- Submit sitemap if not already submitted: `https://example.com/sitemap.xml`
- Check submitted sitemaps for errors
- Remove outdated sitemaps

**Via API:**
```python
python3 scripts/gsc_sitemaps.py --site https://example.com/ --action list
python3 scripts/gsc_sitemaps.py --site https://example.com/ --action submit --sitemap https://example.com/sitemap.xml
```

---

### 4. Core Web Vitals
**Location:** Search Console > Experience > Core Web Vitals

**What it shows:** LCP, INP (replaced FID), and CLS scores for mobile and desktop, grouped by URL cluster.

**Thresholds:**
| Metric | Good | Needs Improvement | Poor |
|--------|------|------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

**What to do with poor scores:**
- LCP: Optimize images (WebP, lazy load), reduce server response time, eliminate render-blocking resources
- INP: Reduce JavaScript execution time, break up long tasks
- CLS: Set explicit width/height on images, avoid inserting content above the fold dynamically

---

### 5. Manual Actions
**Location:** Search Console > Security & Manual Actions > Manual actions

**What it shows:** If Google has penalized the site manually (spam, unnatural links, etc.)

If a manual action exists, address the specific issue and submit a reconsideration request through GSC.

---

### 6. URL Inspection Tool
**Location:** Search Console > URL Inspection (top search bar)

**What it does:** Shows the exact status of a specific URL — when it was crawled, the rendered HTML, coverage status, and enhancements detected.

**When to use:**
- After publishing a new page → request indexing
- After fixing an issue → validate and request re-crawl
- Debugging why a specific page isn't indexed

**Requesting indexing:**
```python
python3 scripts/gsc_inspect_url.py --site https://example.com/ --url https://example.com/page/
```

This only works via the GSC UI (the Indexing API is separate — see below).

---

## Requesting Indexing: Indexing API vs. URL Inspection

| Method | Speed | Scale | Use For |
|--------|-------|-------|---------|
| URL Inspection Tool (GSC UI) | Fast (hours) | 1 URL at a time | Individual pages |
| Google Indexing API | Fast (hours) | Batch, ~200/day | Large sites, job postings, live streams |
| Sitemap submission | Slow (days–weeks) | Entire site | Initial setup, bulk new content |

**Indexing API setup** (requires Google Cloud project + service account):
```python
python3 scripts/gsc_indexing_api.py --url https://example.com/new-page/
```

Note: The Indexing API officially only supports pages with `JobPosting` or `BroadcastEvent` schema. In practice, many sites use it for all pages, but this is against Google's guidelines. Use at your own discretion.

---

## GSC in the SEO Audit Workflow

When running **Audit Mode**, use GSC data as the primary source of truth before making recommendations:

```
1. Pull Performance data (last 90 days):
   - Top 20 queries by impressions
   - Top 20 pages by impressions
   - Pages with CTR < 2% and > 500 impressions (meta tag opportunities)
   - Queries in positions 5–20 (optimization opportunities)

2. Pull Index Coverage:
   - Count errors and identify patterns
   - List "Crawled but not indexed" pages (content quality issue)
   - Check for unexpected "noindex" or robots.txt blocks

3. Pull Core Web Vitals:
   - Flag any URLs with "Poor" LCP, INP, or CLS
   - Note mobile vs. desktop split

4. Check Sitemaps:
   - Confirm sitemap submitted
   - Check for sitemap errors

5. Check Manual Actions:
   - Confirm no penalties
```

Include a GSC summary table in the audit report:

```markdown
### Google Search Console Summary

| Metric | Value |
|--------|-------|
| Total indexed pages | X |
| Index errors | X |
| Avg. CTR | X% |
| Top query | "keyword" (X impressions) |
| Core Web Vitals (mobile) | X Good / X Poor |
| Manual actions | None ✅ / [Issue] ❌ |
| Sitemap submitted | ✅ / ❌ |
```

---

## Quick Wins Checklist from GSC Data

Use this checklist when reviewing GSC data to find high-impact, low-effort improvements:

- [ ] **High impressions, low CTR** → Rewrite meta title/description for those pages
- [ ] **Positions 5–20** → Add more depth, internal links, and schema to push to page 1
- [ ] **Index errors** → Fix 4xx/5xx errors and remove from sitemap if deleted
- [ ] **"Crawled - not indexed"** → Improve content quality or add to internal link structure
- [ ] **Missing sitemap** → Generate and submit `sitemap.xml`
- [ ] **Core Web Vitals failures** → Prioritize LCP fixes (biggest ranking impact)
- [ ] **Duplicate content warnings** → Add canonical tags
- [ ] **Mobile usability issues** → Fix before desktop (Google uses mobile-first indexing)

---

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `gsc_performance.py` | Pulls clicks, impressions, CTR, position by query/page | `python3 scripts/gsc_performance.py --site URL --days 90` |
| `gsc_index_coverage.py` | Lists indexed, error, and excluded pages | `python3 scripts/gsc_index_coverage.py --site URL` |
| `gsc_sitemaps.py` | List, submit, or delete sitemaps | `python3 scripts/gsc_sitemaps.py --site URL --action list` |
| `gsc_indexing_api.py` | Request indexing for a URL | `python3 scripts/gsc_indexing_api.py --url PAGE_URL` |
| `gsc_inspect_url.py` | Get coverage status for a specific URL | `python3 scripts/gsc_inspect_url.py --site URL --url PAGE_URL` |

All scripts use OAuth2 credentials. See setup section above.
