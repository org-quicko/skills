---
name: seo-geo
description: SEO & GEO (Generative Engine Optimization) for websites. Analyze keywords, generate schema markup, optimize for AI search engines (ChatGPT, Perplexity, Gemini, Copilot, Claude) and traditional search (Google, Bing). Use when user wants to improve search visibility, search optimization, search ranking, AI visibility, ChatGPT ranking, Google AI Overview, indexing, JSON-LD, meta tags, or keyword research. Also use when writing or optimizing content for help centre articles, knowledge base pages, discourse forum threads, or any web content that needs to rank well. Covers both auditing existing pages and optimizing new pages before launch. Also use when user mentions Google Search Console, GSC, search performance data, index coverage, crawl errors, Core Web Vitals, sitemap submission, URL inspection, or wants to pull real search query data from their GSC account.
---

# SEO/GEO Optimization Skill

Comprehensive SEO and GEO (Generative Engine Optimization) for websites. Optimize for both traditional search engines (Google, Bing) and AI search engines (ChatGPT, Perplexity, Gemini, Copilot, Claude).

This skill operates in two modes depending on what the user needs:

- **Audit Mode** — Analyze an existing webpage or website, identify SEO/GEO issues, perform keyword research, and produce an actionable report with recommendations.
- **Optimize Mode** — For new or in-progress pages (help centre articles, forum threads, landing pages, etc.), perform keyword research, analyze competitors, and produce ready-to-implement optimizations: meta titles, meta descriptions, JSON-LD schema markup, and content structure recommendations.

Both modes share the same keyword research and SERP analysis foundation. The difference is what comes after: audit mode produces a diagnostic report, optimize mode produces deliverables ready to drop into the page.

## Quick Reference

**GEO = Generative Engine Optimization** — Optimizing content to be cited by AI search engines.

**Key Insight:** AI search engines don't rank pages — they **cite sources**. Being cited is the new "ranking #1".

---

## Workflow

### Step 1: Understand the Context

Before diving in, clarify what you're working with:

- **Existing page?** → Audit Mode. Get the URL, crawl it, identify what's there and what's missing.
- **New page about to go live?** → Optimize Mode. Understand the content, target audience, and business goals.
- **Content being written?** (help articles, forum threads, blog posts) → Optimize Mode. Research keywords first, then guide the writing.

For existing pages, run the technical audit first (Step 2). For new content, skip straight to keyword research (Step 3).

### Step 2: Technical Audit (Audit Mode only)

Analyze the target URL for technical SEO health.

**If the user has Google Search Console access, use GSC data first** — it's the most authoritative source of truth. See [references/google-search-console.md](./references/google-search-console.md) for the full GSC workflow, scripts, and quick wins checklist.

```bash
# Pull real indexing data and search performance
python3 scripts/gsc_performance.py --site https://example.com/ --days 90 --dimension query
python3 scripts/gsc_index_coverage.py --site https://example.com/
python3 scripts/gsc_sitemaps.py --site https://example.com/ --action list
```

**Basic SEO Audit (no GSC access):**
```bash
python3 scripts/seo_audit.py "https://example.com"
```

If the script isn't available, perform the checks manually:

**Check Meta Tags:**
```bash
curl -sL "https://example.com" | grep -E "<title>|<meta name=\"description\"|<meta property=\"og:|application/ld\+json" | head -20
```

**Check robots.txt:**
```bash
curl -s "https://example.com/robots.txt"
```

**Check sitemap:**
```bash
curl -s "https://example.com/sitemap.xml" | head -50
```

**Verify AI Bot Access — these bots should be allowed in robots.txt:**
- Googlebot (Google)
- Bingbot (Bing/Copilot)
- PerplexityBot (Perplexity)
- ChatGPT-User (ChatGPT with browsing)
- ClaudeBot / anthropic-ai (Claude)
- GPTBot (OpenAI)

### Step 3: Keyword Research & SERP Analysis

This is the most critical step. It feeds everything else — meta tags, content structure, schema markup, and GEO optimizations all depend on knowing which keywords to target and what's already ranking.

**If the user has GSC access, start here first** — real search query data beats any keyword tool:
```bash
# Find what queries you already rank for (quick wins)
python3 scripts/gsc_performance.py --site https://example.com/ --days 90 --dimension query --limit 50
# Find which pages drive traffic vs. which are invisible
python3 scripts/gsc_performance.py --site https://example.com/ --days 90 --dimension page --limit 50
```
Look for: (1) queries in positions 5–20 (optimization targets), (2) queries with >500 impressions but <2% CTR (meta tag rewrites needed).

**Read the detailed keyword research procedure** in [references/keyword-research.md](./references/keyword-research.md) before proceeding. That file covers:

1. **Keyword Research via Google Ads Keyword Planner** — Open Chrome, access the Keyword Planner, and collect search volume, competition, and difficulty data. The process differs slightly for existing pages (extract current keywords first, then expand) vs. new pages (start from content analysis and domain context).

2. **SERP Analysis** — Search Google for your primary target keywords and analyze the top-ranking competitors: their content structure, keyword usage, meta titles/descriptions, and how well they align with search intent. This reveals ranking patterns and content gaps you can exploit.

3. **On-Page Keyword Recommendations** — Based on the research, produce a prioritized keyword list and draft optimized meta titles and meta descriptions.

The output of this step should be a **keyword spreadsheet** with columns: Keyword, Search Volume, Competition, Difficulty, Search Intent, and Priority (High / Medium / Low). This spreadsheet becomes the foundation for all optimization work that follows.

### Step 4: GEO Optimization (AI Search Engines)

Apply the **9 Princeton GEO Methods**:

| Method | Visibility Boost | How to Apply |
|--------|-----------------|--------------|
| **Cite Sources** | +40% | Add authoritative citations and references |
| **Statistics Addition** | +37% | Include specific numbers and data points |
| **Quotation Addition** | +30% | Add expert quotes with attribution |
| **Authoritative Tone** | +25% | Use confident, expert language |
| **Easy-to-understand** | +20% | Simplify complex concepts |
| **Technical Terms** | +18% | Include domain-specific terminology |
| **Unique Words** | +15% | Increase vocabulary diversity |
| **Fluency Optimization** | +15-30% | Improve readability and flow |
| ~~Keyword Stuffing~~ | **-10%** | **AVOID — hurts visibility** |

**Best Combination:** Fluency + Statistics = Maximum boost

**Generate FAQPage Schema** (+40% AI visibility):
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is [topic]?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "According to [source], [answer with statistics]."
    }
  }]
}
```

**Content Structure for AI Citability:**
- Use "answer-first" format (direct answer at top of sections)
- Clear H1 > H2 > H3 hierarchy
- Bullet points and numbered lists for scannable info
- Tables for comparison data
- Short paragraphs (2-3 sentences max)
- Include a concise definition or summary near the top that AI engines can extract as a citation

### Step 5: Traditional SEO Optimization

This is where you produce the deliverables. In Audit Mode, these are recommendations. In Optimize Mode, these are ready-to-use outputs.

**Meta Tags — write these based on your keyword research from Step 3:**
```html
<title>{Primary Keyword} - {Secondary Keyword} | {Brand}</title>
<meta name="description" content="{Compelling description with keyword, 150-160 chars}">

<!-- Open Graph -->
<meta property="og:title" content="{Title}">
<meta property="og:description" content="{Description}">
<meta property="og:image" content="{Image URL 1200x630}">
<meta property="og:url" content="{Canonical URL}">
<meta property="og:type" content="website">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{Title}">
<meta name="twitter:description" content="{Description}">
<meta name="twitter:image" content="{Image URL}">
```

**JSON-LD Schema — choose the right type for the page:**
- **WebPage / Article** — for blog posts, articles, and general content pages
- **FAQPage** — for FAQ sections and help centre articles with Q&A format
- **HowTo** — for tutorial and step-by-step guide pages
- **Product** — for product pages
- **Organization** — for about pages
- **SoftwareApplication** — for tools and apps
- **DiscussionForumPosting** — for discourse/forum threads

For each page, generate the complete JSON-LD block with all relevant properties filled in. Don't just suggest the schema type — produce the actual markup the user can paste into their page.

**On-Page SEO Checklist:**
- H1 contains primary keyword
- Images have descriptive alt text with keywords where natural
- Internal links to related content
- External links to authoritative sources (also helps GEO citability)
- Content is mobile-friendly
- Page loads in < 3 seconds

### Step 6: Validate & Monitor

**Google Search Console (primary monitoring tool):**

Read [references/google-search-console.md](./references/google-search-console.md) for the full monitoring workflow. Key tasks:

```bash
# After publishing/updating a page — check its index status
python3 scripts/gsc_inspect_url.py --site https://example.com/ --url https://example.com/new-page/

# Weekly performance check — track clicks, impressions, CTR changes
python3 scripts/gsc_performance.py --site https://example.com/ --days 7 --dimension page

# Ensure sitemap is submitted and healthy
python3 scripts/gsc_sitemaps.py --site https://example.com/ --action list
```

**Request indexing for new/updated pages:**
- Open GSC > URL Inspection > paste URL > click "Request Indexing" (browser UI only, not scriptable)
- Or submit/update your sitemap to signal new content to Google

**Schema Validation:**
```bash
open "https://search.google.com/test/rich-results?url={encoded_url}"
open "https://validator.schema.org/?url={encoded_url}"
```

**Check Indexing Status:**
```bash
open "https://www.google.com/search?q=site:{domain}"
open "https://www.bing.com/search?q=site:{domain}"
```

**Generate Report** (Audit Mode) or **Deliver Optimizations** (Optimize Mode):

For **Audit Mode**, produce a report:
```markdown
## SEO/GEO Optimization Report for [URL]

### Current Status
- Meta Tags: ✅/❌
- Schema Markup: ✅/❌
- AI Bot Access: ✅/❌
- Mobile Friendly: ✅/❌
- Page Speed: X seconds

### Keyword Analysis Summary
[Link to keyword spreadsheet]

### Priority Recommendations
1. [Highest-impact action]
2. [Second priority]
3. [Third priority]

### GEO Optimizations Needed
- [ ] FAQPage schema
- [ ] Statistics and citations in content
- [ ] Answer-first content structure
```

For **Optimize Mode**, deliver:
- Complete meta title and description (ready to paste)
- Complete JSON-LD schema markup (ready to paste)
- Keyword-optimized content suggestions or edits
- FAQPage schema if applicable

---

## Platform-Specific Optimization

Different AI search engines weight different signals. Tailor your approach based on where your audience searches.

### ChatGPT
- Focus on **branded domain authority** (cited 11% more than third-party)
- Update content within **30 days** (3.2x more citations)
- Build **backlinks** (>350K referring domains = 8.4 avg citations)
- Match content style to ChatGPT's response format

### Perplexity
- Allow **PerplexityBot** in robots.txt
- Use **FAQ Schema** (higher citation rate)
- Host **PDF documents** (prioritized for citation)
- Focus on **semantic relevance** over keywords

### Google AI Overview (SGE)
- Optimize for **E-E-A-T** (Experience, Expertise, Authority, Trust)
- Use **structured data** (Schema markup)
- Build **topical authority** (content clusters + internal linking)
- Include **authoritative citations** (+132% visibility)

### Microsoft Copilot / Bing
- Ensure **Bing indexing** (required for citation)
- Optimize for **Microsoft ecosystem** (LinkedIn, GitHub mentions help)
- Page speed **< 2 seconds**
- Clear **entity definitions**

### Claude AI
- Ensure **Brave Search indexing** (Claude uses Brave, not Google)
- High **factual density** (data-rich content preferred)
- Clear **structural clarity** (easy to extract)

---

## Content-Type Guidance

When optimizing specific content types, keep these patterns in mind:

**Help Centre / Knowledge Base Articles:**
- Use FAQPage or HowTo schema
- Lead with the answer (users searching for help want solutions fast)
- Include the exact phrasing people use when asking for help (matches voice search and AI queries)
- Structure with clear headings that mirror common questions

**Discourse / Forum Threads:**
- Use DiscussionForumPosting schema
- First post should be comprehensive (search engines index the opening post most heavily)
- Include relevant keywords naturally in the title and opening paragraph
- Link to related documentation or resources

**Landing Pages:**
- Use WebPage or Product schema depending on context
- Meta description should be action-oriented (drives CTR)
- Include social proof signals (statistics, testimonials) for both SEO and GEO

---

## Skill Dependencies

This skill works best with:
- **Chrome browser tools** — For Google Ads Keyword Planner research
- **xlsx skill** — For producing keyword research spreadsheets
- **WebSearch** — For SERP analysis and competitor research
- **Google Search Console** — For real performance data, index coverage, and Core Web Vitals (see [references/google-search-console.md](./references/google-search-console.md))
