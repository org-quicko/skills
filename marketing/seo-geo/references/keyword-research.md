# Keyword Research & SERP Analysis — Detailed Procedure

This reference covers the full keyword research workflow. It's called from Step 3 of the main SKILL.md.

## Table of Contents

1. [Keyword Research via Google Ads Keyword Planner](#1-keyword-research-via-google-ads-keyword-planner)
2. [SERP Analysis](#2-serp-analysis)
3. [On-Page Keyword Recommendations](#3-on-page-keyword-recommendations)
4. [Output Format](#4-output-format)

---

## 1. Keyword Research via Google Ads Keyword Planner

Use Chrome browser tools to access Google Ads Keyword Planner. This provides actual search volume and competition data, which is far more reliable than estimating from third-party tools via web search.

### Getting to Keyword Planner

1. Open Chrome and navigate to `https://ads.google.com/aw/keywordplanner/home`
2. If prompted to sign in, ask the user to authenticate (do not enter credentials)
3. Once in Keyword Planner, you'll see two options:
   - **"Discover new keywords"** — Use this for finding new keyword opportunities
   - **"Get search volume and forecasts"** — Use this when you already have a keyword list and need data

### For Existing Webpages (Audit Mode)

When auditing a page that's already live, start by understanding what it currently targets, then expand.

**Phase 1 — Extract current keywords:**
- Read the page content (from the audit in Step 2)
- Identify the keywords the page appears to be targeting based on:
  - The H1 and page title
  - Recurring terms in headings and body text
  - Meta description content
  - Alt text on images
- Note any keyword gaps — topics the page covers but doesn't explicitly target

**Phase 2 — Research in Keyword Planner:**
- In Keyword Planner, choose "Discover new keywords"
- Use "Start with a website" and enter the page URL to let Google analyze it
- Also try "Start with keywords" using the keywords you extracted in Phase 1
- For each result, collect:
  - **Search volume** (average monthly searches)
  - **Competition level** (Low / Medium / High)
  - **Keyword difficulty** (if shown — this indicates how hard it is to rank)
  - **Top of page bid** (low range and high range — this is a proxy for commercial value)
- Filter and sort results by relevance to the page's topic
- Look for keywords with decent volume but lower competition — these are your opportunities

**Phase 3 — Expand and prioritize:**
- Identify additional relevant keywords the page isn't targeting
- Group keywords by search intent:
  - **Informational** — "what is X", "how to X" (good for help articles, guides)
  - **Navigational** — "[brand] X", "[product] login" (good for branded pages)
  - **Commercial** — "best X", "X vs Y", "X reviews" (good for comparison pages)
  - **Transactional** — "buy X", "X pricing", "X free trial" (good for product/landing pages)
- Create a prioritized list based on: relevance to page content, search volume, competition level, and alignment with business goals

### For New Webpages (Optimize Mode)

When the page hasn't been published yet, you're starting from the content draft and business context.

**Phase 1 — Understand the content and context:**
- Read the draft content (or content brief) the user has provided
- Understand the broader domain: What does the website/product do? Who is the audience?
- Identify the core topic and sub-topics the page covers

**Phase 2 — Seed keyword discovery:**
- Brainstorm seed keywords based on the content topic
- In Keyword Planner, choose "Discover new keywords" → "Start with keywords"
- Enter 3-5 seed keywords that describe the page's core topic
- Also try "Start with a website" using the domain's homepage or a competitor URL to see what Google associates with the space

**Phase 3 — Build the keyword list:**
- From the Keyword Planner results, identify:
  - **Primary keywords** (1-2) — The main terms the page should rank for. High relevance, good volume.
  - **Secondary keywords** (3-5) — Supporting terms that reinforce the topic. Include in subheadings and body text.
  - **Long-tail keywords** (5-10) — Specific, lower-volume phrases that are easier to rank for and often match voice/AI search queries. These are especially valuable for help centre articles and forum threads.
- Collect search volumes and competition metrics for all of them
- Prioritize based on the balance between relevance, volume, and ranking potential

---

## 2. SERP Analysis

After identifying your target keywords, search for them on Google to understand what's currently ranking and why. This reveals what search engines consider "good content" for these queries.

### How to Perform SERP Analysis

1. **Search Google for each primary keyword** using Chrome browser tools
2. For the top 5-10 results, analyze:

**Content structure:**
- How long is the content? (word count gives a rough benchmark)
- What headings do they use? (reveals the subtopics Google expects)
- Do they use lists, tables, images, videos?
- Is the content a guide, a list, a comparison, a FAQ?

**Keyword usage:**
- Where do they place the primary keyword? (title, H1, first paragraph, URL)
- What related terms and synonyms appear?
- How naturally are keywords integrated vs. feeling forced?

**Meta titles and descriptions:**
- What patterns do the top results follow?
- How long are the titles? (typically 50-60 characters)
- Do descriptions include calls to action?
- What emotional triggers or value propositions do they use?

**Search intent alignment:**
- Does the content type match the query intent?
  - Informational query → guide, tutorial, explainer
  - Commercial query → comparison, review, "best of" list
  - Transactional query → product page, pricing page
- Pages that mismatch intent rarely rank well regardless of their keyword optimization

3. **Identify opportunities:**
   - Content gaps — topics the top results don't cover well
   - Freshness gaps — outdated information you can improve on
   - Format gaps — if everyone writes long guides but the query would be better served by a concise FAQ, that's an opportunity
   - Schema gaps — if competitors lack structured data, adding it gives you an edge in rich results and AI citations

---

## 3. On-Page Keyword Recommendations

Based on the keyword research and SERP analysis, produce these deliverables:

### Optimized Meta Title
- Include the primary keyword, ideally near the beginning
- Keep under 60 characters (Google truncates longer titles)
- Make it click-worthy — not just keyword-stuffed
- Pattern: `{Primary Keyword} — {Value Proposition} | {Brand}`
- Example: `Industrial PLC Programming Guide — Step-by-Step Tutorial | OPC Skills`

### Optimized Meta Description
- Include the primary keyword naturally
- Keep between 150-160 characters
- Include a call to action or value statement
- Address the search intent directly
- Pattern: `{What the page delivers}. {Why it's valuable}. {CTA}.`
- Example: `Learn PLC programming from scratch with our hands-on tutorial. Covers ladder logic, function blocks, and real-world examples. Start building today.`

### Keyword Placement Recommendations
- **H1** — Primary keyword, phrased naturally
- **First 100 words** — Primary keyword should appear early
- **H2s** — Secondary keywords as subheading topics
- **Body text** — Long-tail keywords woven in naturally throughout
- **Image alt text** — Descriptive, keyword-relevant where appropriate
- **URL slug** — Short, keyword-rich (e.g., `/plc-programming-guide`)

---

## 4. Output Format

The keyword research should be delivered as a structured spreadsheet (use the xlsx skill if available). The spreadsheet should have these columns:

| Column | Description |
|--------|-------------|
| **Keyword** | The keyword or phrase |
| **Search Volume** | Average monthly searches (from Keyword Planner) |
| **Competition** | Low / Medium / High (from Keyword Planner) |
| **Difficulty** | Keyword difficulty score if available |
| **Search Intent** | Informational / Navigational / Commercial / Transactional |
| **Priority** | High / Medium / Low (your assessment based on relevance + volume + ranking potential) |
| **Notes** | Any relevant context — e.g., "currently ranking #8", "competitor gap", "long-tail opportunity" |

Sort by Priority (High first), then by Search Volume (descending).

If the xlsx skill is not available, output the data as a markdown table or CSV. The important thing is that the user gets a structured, sortable artifact they can work with — not just a list buried in prose.