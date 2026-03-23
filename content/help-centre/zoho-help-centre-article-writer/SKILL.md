---
name: zoho-help-centre-article-writer
description: Write, edit, and publish help centre articles directly to Zoho Desk. Supports all four Diátaxis documentation types, tutorials, how-to guides, reference, and explanation articles. Follows best-in-class writing standards inspired by Slack and Notion help centres. Accepts any input, text descriptions, screenshots, screen recordings, images, existing docs, or just a topic. Fetches categories dynamically from Zoho Desk and publishes articles in-place. Integrates with the seo-geo skill for keyword research and on-page SEO when needed. Use this skill whenever someone asks to write a help article, update an existing knowledge base article, draft help centre content, create a tutorial, how-to guide, reference page, or explainer, or publish documentation to Zoho Desk. Also trigger when the user mentions help centre, knowledge base, KB article, support article, Zoho Desk article, or any help centre URL — even casually.
---

# Help Centre Article Writer

Write and publish help centre articles to Zoho Desk. Articles follow a writing standard modelled on the best help centres in the industry (Slack, Notion) — clear, concrete, respectful of the reader's time.

---

## Before You Write: Gather Context

Every article starts by understanding what you're working with. Get clarity on these before writing a word.

### 1. What has the user given you?

Users can provide source material in any form. Your job is to extract the substance and turn it into a well-structured article — regardless of how the input arrives.

**Common inputs and how to handle them:**

- **A topic or feature name** ("write about workspace roles") — You'll need to ask clarifying questions: who's the audience, what should the article cover, what does the feature actually do?
- **Screenshots or images** — Study them. Extract UI labels, navigation paths, field names, and the sequence of actions shown. These are often the most accurate source of truth for how-to articles. Reference what you see in the screenshots when writing steps.
- **Multiple screenshots showing a flow** — Reconstruct the step-by-step sequence from the images. Each screenshot likely represents one or more steps. Map them in order before writing.
- **A screen recording or video** — Watch/process it and extract the actions taken, the screens visited, and the outcome. Translate into written steps.
- **An existing document, draft, or notes** — Read it, extract the core information, and reshape it into proper help centre structure. Don't just reformat — rewrite with the writing principles below.
- **A conversation or Slack thread** — Pull out the factual content and decisions. Discard the back-and-forth. Structure what remains.
- **A mix of the above** — Synthesise across all inputs. Screenshots might show the UI flow while a text description provides the "why". Combine them.

The key principle: never reject or constrain what the user provides. Adapt to whatever they give you and extract maximum value from it.

### 2. Which Zoho Desk organisation and category?

Ask the user for their **Zoho Org ID** (or confirm it if you've used it before in this conversation). Then fetch the category tree:

```
Use ZohoDesk_getAllKBRootCategories with the orgId to list root categories.
Then use ZohoDesk_getKBRootCategoryTree on the relevant root category to see the full hierarchy.
```

Present the category options to the user and let them pick. If no existing category fits, ask whether they'd like to place it in the closest match or create a new one (note: creating sections/subcategories requires manual setup in Zoho Desk if the MCP tools for section creation aren't available).

### 3. Which article type?

Articles follow the Diátaxis framework — four types, each serving a different reader need. Picking the right type is about understanding *why the reader is here*.

**Tutorial** — A learning-oriented lesson that guides a beginner through a complete experience.
The reader is new and wants to *learn by doing*. A tutorial takes them from zero to a working result, building confidence along the way. The focus is on the learning journey, not just the end state. Titles often frame the experience: "Get Started with Your First Workspace", "Build Your First API Integration", "Set Up Your Team in 10 Minutes".

**How-To Guide** — A task-oriented set of steps for accomplishing a specific goal.
The reader already has context and wants to *get something done*. They know what they need — they just need the steps. Unlike a tutorial, a how-to assumes some baseline knowledge and gets straight to the procedure. Titles are action-oriented: "Invite Team Members to Your Workspace", "Connect a Custom Domain", "Export Your Data".

**Reference** — An information-oriented description of the system as it is.
The reader needs to *look something up* — a field definition, an API parameter, a list of permissions, a configuration option. Reference articles are structured for scanning, not reading start-to-finish. They're accurate, complete, and consistently formatted. Titles name the thing being documented: "Workspace Roles and Permissions", "API Rate Limits", "Billing Plan Comparison".

**Explanation** — An understanding-oriented discussion that clarifies concepts and context.
The reader wants to *understand why* — why the system works this way, what a concept means in practice, how different parts connect. Explanations provide the thinking behind the design. Titles frame the concept: "How Billing Works", "Understanding Role-Based Access", "What Happens When You Archive a Workspace".

**How to choose:**

| Reader's mindset | They want to... | Article type |
|---|---|---|
| "I'm new, show me" | Learn by following along | **Tutorial** |
| "I need to do X" | Complete a specific task | **How-To Guide** |
| "What are the options?" | Look up specific information | **Reference** |
| "Why does it work this way?" | Understand a concept | **Explanation** |

If the user's request doesn't map neatly to one type, ask. And if a topic naturally spans two types (e.g., an explanation of billing that also includes how to upgrade), split it into separate articles and link between them.

### 4. New or update?

- **New article** → Draft from scratch, then create via Zoho Desk MCP.
- **Update existing** → Fetch the current article via `ZohoDesk_getArticle`, review it, revise, then push the update via `ZohoDesk_updateArticle`.

When updating, show the user what's currently there and what you plan to change before pushing.

---

## Writing Principles

These principles are non-negotiable. They're what separate a help centre people actually use from one people bounce off.

### Every sentence earns its place

This is the single most important principle. If a sentence doesn't tell the reader something concrete they didn't already know, cut it. Help centre readers are task-focused — they arrived with a problem and want a solution. Respect that by getting to the point.

**What filler looks like:**
> "Managing your team is easy with our platform. In just a few steps, you can invite colleagues to collaborate and assign them the right permissions from day one."

This says nothing. "Managing your team is easy" is a marketing claim. "In just a few steps" is padding. "From day one" is filler. The reader learns nothing from these two sentences.

**What concrete writing looks like:**
> "Invite team members to your Workspace so they can access API keys, reports, and billing. You can assign roles to control what each member can do."

Two sentences. The reader now knows *what* they'll do, *why*, and *what they can control*. Zero wasted words.

**Another example — a good feature intro:**
> "A workspace is where you manage API keys, teams, billing, and more. Create one to start using the APIs."

Immediate, concrete, done. Study this pattern. The reader knows what a workspace contains and what to do next.

### Before finalising any article, cut these

Go through the draft and actively remove:

- **Filler openers**: "This makes it easy to...", "With X, you can easily...", "In just a few steps..." — rewrite to state the action directly.
- **Empty adjectives**: "powerful", "robust", "comprehensive", "intuitive", "seamless", "effortless" — these describe nothing. If a feature is genuinely powerful, explain *what it does* that makes it so.
- **Title restatements**: Any sentence that just restates what the heading already says.
- **Bridge sentences**: Transition sentences that exist only to connect sections. The heading does that job.
- **Vague future promises**: "streamline your workflow", "boost your productivity" — say what the thing concretely does instead.

### Voice and mechanics

- **Second person.** Address the reader as "you" / "your". You're talking to one person helping them solve one problem.
- **Present tense.** "Click the button" not "You will click the button".
- **Active voice.** "The system sends a confirmation email" not "A confirmation email is sent by the system".
- **Short sentences.** If a sentence has more than one comma, consider splitting it. Paragraphs stay at 2–3 sentences.
- **Conversational but not casual.** Sound like a knowledgeable colleague explaining something at a whiteboard — clear, direct, helpful, without being stiff or corporate. Not overly formal, not chatty.
- **Bold for UI elements** using HTML `<strong>` tags (Zoho Desk renders HTML, not markdown). Example: Click <strong>Settings</strong> from the sidebar.
- **No jargon without context.** If a term might be unfamiliar to the reader, briefly explain it on first use. Don't assume everyone shares your vocabulary.

### Anchor abstract concepts with concrete language

When explaining something conceptual, make it tangible. Instead of "Databases provide flexible data management capabilities", write something like "A database lets you track tasks, organise notes, or manage a content calendar — and switch between table, board, and calendar views of the same data." The reader can picture it.

This doesn't mean every article needs metaphors. It means every explanation should connect to something the reader already understands or can immediately visualise.

### One purpose per article

Each article serves exactly one purpose. A how-to covers one procedure. A reference documents one system or entity. A tutorial teaches one complete skill. An explanation clarifies one concept.

If a topic involves multiple distinct actions, break it into separate articles and link between them:

- "How to Upload Documents to Drive" (how-to)
- "How to Share Documents with Your Team" (how-to)
- "Understanding Drive Permissions" (explanation)
- "Drive Storage Limits and File Types" (reference)

If you find yourself writing two sets of numbered steps under different headings, that's a sign you need two articles. If a how-to keeps pausing to explain background concepts, split the explanation into its own article and link to it. When the user asks for a broad topic like "write about Drive", propose a set of articles across the relevant types and write them individually.

### State prerequisites and permissions upfront

If an action requires a specific role, plan, or prerequisite, say so *before* the steps — not buried in step 4 where the reader discovers they can't proceed. This is one of the most common sources of reader frustration in help centres.

Place permission and prerequisite information in a "Before You Start" or "Things to Keep in Mind" section immediately after the intro, before the steps begin.

---

## Article Templates

The article body is HTML for Zoho Desk. Use proper HTML tags throughout:

- `<strong>` for bold (never markdown `**`)
- `<em>` for italics (never markdown `*`)
- `<ol>` and `<li>` for numbered steps
- `<ul>` and `<li>` for bullet lists
- `<h1>`, `<h2>`, `<h3>` for headings
- `<table>`, `<tr>`, `<th>`, `<td>` for tables
- `<p>` for paragraphs
- `<a href="...">` for links

Do not include `<style>`, `<head>`, `<!DOCTYPE>`, or CSS. Output only the article body HTML — Zoho Desk handles the wrapper and styling.

### Tutorial

Tutorials guide beginners through a complete experience. The reader should feel a sense of progress and end with something that works.

```html
<h1>[Experience-framing title — e.g., "Get Started with Your First Workspace"]</h1>

<p>[1–2 sentences: what the reader will build or accomplish by the end. Frame it as a journey with a concrete outcome. Example: "By the end of this guide, you'll have a working workspace with your first API key ready to use."]</p>

<h2>What You'll Need</h2>

<ul>
  <li>[Prerequisite — e.g., an account, a specific role, a tool installed.]</li>
  <li>[Prerequisite — keep this list short. If there are many, the tutorial scope is too broad.]</li>
</ul>

<h2>[First milestone heading — e.g., "Create Your Workspace"]</h2>

<ol>
  <li><strong>[Action verb + what to do]</strong> — [Brief context. For tutorials, err on the side of more explanation since the reader is new.]</li>
  <li><strong>[Action verb + what to do]</strong> — [What they should see or expect after this step.]</li>
</ol>

<h2>[Second milestone heading — e.g., "Generate Your First API Key"]</h2>

<ol>
  <li><strong>[Action verb + what to do]</strong> — [Context.]</li>
  <li><strong>[Action verb + what to do]</strong> — [Context.]</li>
</ol>

<h2>What You've Built</h2>

<p>[1–2 sentences summarising what the reader now has. Reinforce the accomplishment. Then point them to what to explore next — link to related how-to guides or explanations.]</p>

<h2>Need Help?</h2>

<p>[Closing CTA.]</p>
```

**Tutorial writing principles:**
- Structure around milestones, not just steps. Each H2 section should feel like a small accomplishment.
- Explain more than in a how-to. The reader is learning, not just executing. Brief "why" context after steps helps build understanding.
- Keep the scope tight. A tutorial that takes more than 10–15 minutes to complete is probably too broad — split it.
- End with a sense of completion. The reader should feel they've built or achieved something real.
- Link forward to how-to guides for the natural next actions ("Now that you have a workspace, learn how to invite your team").

### How-To Guide

How-to guides are for readers who already know what they want to do and just need the steps.

```html
<h1>[Action-oriented title — one specific task]</h1>

<p>[1–2 sentences: what the reader will accomplish and why it matters. State the concrete outcome. No filler.]</p>

<h2>Before You Start</h2>

<ul>
  <li><strong>[Prerequisite or permission]:</strong> [What the reader needs to know — required role, plan, or setup step.]</li>
  <li><strong>[Key concept]:</strong> [Any context that prevents confusion during the steps.]</li>
</ul>

<h2>[Main action heading — e.g., "Invite a Team Member"]</h2>

<ol>
  <li><strong>[Action verb + what to do]</strong> — [Brief context or what happens next.]</li>
  <li><strong>[Action verb + what to do]</strong> — [Brief context.]</li>
  <li><strong>[Action verb + what to do]</strong> — [Brief context.]</li>
</ol>

<p><strong>Note:</strong> [Any important caveat or edge case the reader should know.]</p>

<h2>Need Help?</h2>

<p>[Closing CTA.]</p>
```

**How-to writing principles:**
- Each step = one action. Don't combine "click Settings and then select Billing" into one step.
- Start each step with a strong verb: Click, Select, Enter, Navigate, Review, Submit, Download, Toggle, Expand.
- After the bold action, add a dash and explain *why* or *what happens* — but only when it adds value.
- Include UI navigation paths: "Go to <strong>Settings</strong> > <strong>Billing</strong> > <strong>Plans</strong>."
- When multiple methods exist for the same action (keyboard shortcut, menu click, etc.), present them as alternatives within the step or as a brief note — don't create separate step sequences unless the paths meaningfully diverge.
- Unlike tutorials, how-to guides skip the "why" and get straight to the procedure. If the reader needs background, link to an explanation article.

### Reference

Reference articles are structured for scanning and lookup, not linear reading. They document the system as it is — complete, accurate, and consistently formatted.

```html
<h1>[Name of the thing being documented — e.g., "Workspace Roles and Permissions"]</h1>

<p>[1–2 sentences: what this reference covers and when the reader would use it. Example: "This page lists all workspace roles, what each role can access, and how permissions are inherited."]</p>

<h2>[Category or grouping heading — e.g., "Role Types"]</h2>

<table>
  <tr><th>Role</th><th>Description</th><th>Can manage billing</th><th>Can invite members</th></tr>
  <tr><td><strong>Owner</strong></td><td>Full access to all settings and data.</td><td>Yes</td><td>Yes</td></tr>
  <tr><td><strong>Admin</strong></td><td>Manages team and settings. Cannot delete the workspace.</td><td>Yes</td><td>Yes</td></tr>
  <tr><td><strong>Member</strong></td><td>Standard access. Can use features but not change settings.</td><td>No</td><td>No</td></tr>
</table>

<h2>[Another grouping — e.g., "Permission Details"]</h2>

<ul>
  <li><strong>[Term or field]</strong> — [Precise definition. No ambiguity.]</li>
  <li><strong>[Term or field]</strong> — [Precise definition.]</li>
</ul>

<h2>[Optional: related notes or edge cases]</h2>

<p>[Any caveats, version-specific behaviour, or exceptions.]</p>

<h2>Need Help?</h2>

<p>[Closing CTA.]</p>
```

**Reference writing principles:**
- Optimise for scanning. Tables, definition lists, and consistent formatting matter more than prose here.
- Be exhaustive within scope. If you're documenting roles, document *all* roles. A reference that's missing entries erodes trust.
- Use consistent structure. If one role entry has columns for "Description", "Can manage billing", "Can invite members", every role entry must have the same columns.
- Keep descriptions factual and precise. Reference articles describe what *is*, not what's recommended. Save advice for how-to guides.
- Alphabetical or logical ordering — pick one and stick with it within each section.
- Link to how-to guides for "how do I change this?" and explanation articles for "why does it work this way?".

### Explanation

Explanation articles help the reader build a mental model of how something works and why it was designed that way.

```html
<h1>[Concept-framing title — e.g., "How Billing Works"]</h1>

<p>[1–2 sentences: what this article explains, framed around the reader's likely question. Example: "This article explains how billing is calculated, when charges occur, and what happens when you change plans mid-cycle."]</p>

<h2>[First concept heading — e.g., "How Charges Are Calculated"]</h2>

<p>[Explanation — 2–4 sentences. Use concrete examples. Connect abstract concepts to things the reader already understands. Example: "Your monthly charge is based on the number of active seats in your workspace at the end of each billing cycle. If you add 3 members on the 15th of the month, you're charged for half a month for those seats."]</p>

<h2>[Second concept heading — e.g., "What Happens When You Change Plans"]</h2>

<p>[Explanation. Use scenarios or examples to make abstract behaviour tangible.]</p>

<h2>[Optional: how things connect — e.g., "Billing and Workspace Roles"]</h2>

<p>[Explain the relationship between this concept and related concepts. Link to the relevant reference or how-to articles.]</p>

<h2>Need Help?</h2>

<p>[Closing CTA.]</p>
```

**Explanation writing principles:**
- Lead with the "what" and "why" — don't bury the core concept.
- Use concrete scenarios and examples. "If you add 3 members on the 15th, you're charged half a month" is better than "charges are prorated".
- Connect concepts to each other. Explanations are where you show how different parts of the system relate.
- Use subheadings that tell a story. A reader scanning the headings alone should get the gist of the explanation.
- Don't include step-by-step instructions — link to the relevant how-to guide instead.
- Tables and diagrams can help when explaining comparisons, flows, or hierarchies.
- Bold key terms on first use, especially terms that appear in reference articles (and link to them).

---

## Linking Related Articles

Good help centres connect articles into a web of knowledge rather than leaving each one as an island. The Diátaxis types are designed to link to each other:

- **Tutorials** link forward to **how-to guides** ("Now that you've set up your workspace, learn how to invite your team") and to **explanations** for deeper context.
- **How-to guides** link to **reference** articles for lookup details and to **explanations** when a step involves a concept that might be unfamiliar.
- **Reference** articles link to **how-to guides** for "how do I change this?" and to **explanations** for "why does it work this way?".
- **Explanations** link to **how-to guides** for the practical "now go do it" and to **reference** articles for precise specifications.
- **All types** can link to prerequisite articles in their opening section.

To find existing articles for linking, use `ZohoDesk_getArticles` filtered by `categoryId` or search by topic. Use the article's permalink or Zoho help centre URL for the `<a href>` tag.

---

## SEO Optimisation

For every article, follow these baseline SEO practices:

- Use the primary topic keyword in the H1 title.
- Use descriptive H2 headings that mirror how people search for help (not generic labels like "Step 1").
- Keep the title under 60 characters where possible.
- Structure content with a clear H1 > H2 > H3 hierarchy.

**When the user requests a full SEO pass**, invoke the `seo-geo` skill. It will handle keyword research, meta tag crafting, and schema markup recommendations. When publishing to Zoho after an SEO pass, include the `seoTitle`, `seoDescription`, and `seoKeywords` fields in the create/update call.

Even without a full SEO pass, write titles and headings in the language your readers would use when searching. "How to Reset Your Password" is more searchable than "Password Management Procedures".

---

## Review Before Publishing

Never publish or push to Zoho Desk without the user reviewing the draft first. This is a hard rule — no exceptions, even if the user said "just publish it" at the start. People change their minds once they see the actual content.

**The review flow:**

1. **Present the full draft** to the user — the complete HTML article body, the proposed title, and the category you plan to publish to. Show it clearly so they can read through it.
2. **Ask for feedback.** Explicitly ask: "Here's the draft. Want me to change anything before publishing?" Don't just ask "looks good?" — invite them to actually review.
3. **Incorporate changes.** If the user has edits, make them and show the revised version. Repeat until they're happy.
4. **Only then confirm publishing details** — category, status (Draft/Published/Review), and tags.
5. **Publish to Zoho Desk** only after the user gives a clear go-ahead on both the content and the publishing details.

For updates to existing articles, the same flow applies: show the current version, show your proposed changes (ideally highlighting what's different), get feedback, revise, then push.

---

## Publishing to Zoho Desk

### Choosing the right category

1. Fetch the category tree using `ZohoDesk_getAllKBRootCategories` and `ZohoDesk_getKBRootCategoryTree` with the user's orgId.
2. Match the article's topic to the most specific category or section available.
3. If the match is clear, propose it to the user: "I'll place this under [Category Name] — does that work?"
4. If the topic could fit multiple categories, present the options and let the user choose.
5. If nothing fits, ask the user — don't guess.

### Creating a new article

After the user has reviewed and approved the draft, use `ZohoDesk_createArticle` with:

```
body:
  title: "Your Article Title"
  answer: "<html content>"
  categoryId: "<from the category tree>"
  status: "<Draft | Published | Review>"
  permission: "ALL"  (unless the user specifies otherwise)
  tags: ["relevant", "tags"]

query_params:
  orgId: "<user's org ID>"
```

Confirm with the user:
1. The category (propose one from the tree based on the topic).
2. The status — Draft, Published, or Review?

If SEO fields are available from an seo-geo pass, also include `seoTitle`, `seoDescription`, `seoKeywords`, and `permalink`.

### Updating an existing article

1. Fetch the article using `ZohoDesk_getArticle` with the article ID and orgId.
2. Show the user what's currently there.
3. Show your proposed changes — highlight what's different where possible.
4. Get the user's feedback and incorporate revisions.
5. Only after approval, use `ZohoDesk_updateArticle` with the revised content.

### Listing and searching articles

Use `ZohoDesk_getArticles` to list articles, optionally filtered by:
- `categoryId` — filter by category
- `status` — Draft, Published, Review, Expired, Unpublished
- `sortBy` — createdTime, modifiedTime, viewCount, etc.

This is useful when the user wants to audit existing articles, find articles to link to, or review what's already published in a category.

---

## Common Mistakes

- **Filler intros.** "Managing your team is easy with Console" is marketing copy. Write: "Invite team members to your Workspace so they can access API keys and reports." Every sentence delivers concrete information.
- **Markdown in the output.** The output is HTML for Zoho Desk. Use `<strong>` not `**`, `<em>` not `*`. No CSS, no `<style>`, no `<head>` — just article body HTML.
- **Skipping the intro.** Every article needs 1–2 sentences of context before diving in. Context is not filler — it tells the reader they're in the right place.
- **Burying prerequisites.** If a feature requires admin access or a paid plan, say so immediately after the intro — not in the middle of step 3.
- **Vague steps.** "Configure the settings" is not a step. "Go to <strong>Settings</strong> > <strong>Billing</strong> and select your plan" is.
- **Combining multiple actions in one step.** Each numbered step should be one discrete action.
- **Over-engineering.** Don't add FAQ sections, troubleshooting sections, or best practices unless the user asks for them. Keep the article focused on its single purpose.
- **Walls of text.** If a section exceeds 4–5 sentences, it needs a subheading or a list to break it up.
- **Publishing without a review cycle.** Always show the full draft and ask for feedback before publishing. Don't skip straight to Zoho — even if the user initially said "just publish it".
- **Orphaned articles.** When writing a new article, check if there are related articles that should link to it (and vice versa).
