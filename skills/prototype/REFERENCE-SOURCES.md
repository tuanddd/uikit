# Reference sources

The rule this file exists to enforce: **when you need to know how a step should work, the answer comes from a product that shipped it, not from your taste.** You are the builder, so nobody else will ask the question, which is exactly why you ask it of yourself. Nearly every question (what step 2 asks that step 1 did not, what the empty state offers, where the confirmation number lives) has been answered by a team that ran it past real users. Go and look.

## Mobbin is paid: check it first

Mobbin's MCP server comes with a paid Mobbin plan. Phase 0 checks it before any other work, so the user knows whether the run uses it and what the fallback costs:

```
ToolSearch("+mobbin")
```

| Result | Tell the user | Then |
|---|---|---|
| `mcp__mobbin__*` tools load | "Mobbin MCP is connected. It is a paid service; this run uses it for the reference lookups, about one search per step." | Continue. The first lookup doubles as the auth check |
| No Mobbin tool | "Mobbin MCP is not connected. It comes with a paid Mobbin plan and is where this skill finds how shipped products solved each step. Connect it and rerun, or continue on free sources, where more decisions rest on a principle instead of a reference." | Wait for the answer |
| A lookup fails with an auth or quota error | The error, and the same two choices | Wait for the answer |

## The two primary sources

### Mobbin — MCP server first, `https://mobbin.com` second

The largest indexed corpus of real shipped app and web screens and multi-screen flows. It answers *"what does step 2 actually show"*, because it captures flows as ordered sequences rather than isolated screens.

**Route 1, the MCP server.** Structured results, flow sequences as data, no blur, no sign-in wall, no browser tab. When Phase 0 loaded the tools, every Mobbin lookup goes through them: search flows by flow name, screens for one state, sections for one part of a page. Bank the rows with `Mobbin MCP — <app>, <n>-screen flow` as the source. Do not open the website while the MCP route works.

**Route 2, the website in the user's Chrome.** Only when the user chose it after Phase 0 found no tool or a failing one. Say which route you are on; the notes below apply.

**Access reality:** the free tier is limited and blurs much of the corpus; flows in particular are the paywalled part of this market. `browser-harness` drives the user's own running Chrome, so their Mobbin session is already yours: if they are signed in, you are signed in. If you hit a blur or a wall:

1. Tell them plainly: "Mobbin is showing a sign-in wall. Sign in in the browser window, or say skip and I'll use the free sources."
2. Wait for their explicit continue, then retry the same tab.
3. **Never** route around it: no unblur extension, no scraping the gate, no logged-out trick. Hard Rule 9 in SKILL.md is not negotiable.

Mining pattern:

```bash
browser-harness <<'PY'
new_tab("https://mobbin.com/discover/apps/web/latest")
wait_for_load()
print(js("document.body.innerText.slice(0, 2000)"))
PY
```

Open one tab for the research and reuse it for every lookup: `new_tab()` on the first call, `goto_url()` after that. Filtered listings are reachable by URL once you know the taxonomy, which beats clicking through the UI. To capture a flow visually, into the session's scratchpad:

```bash
browser-harness <<'PY'
import base64, pathlib
data = cdp("Page.captureScreenshot", format="png")["data"]
pathlib.Path("<scratchpad>/ref-flow.png").write_bytes(base64.b64decode(data))
PY
```

On either route, search by **flow name, not app name**: "booking confirmation", "empty search results", "identity verification", "contact host". You want the pattern across many products, not one product's whole app. Match the platform the feature ships on: web for a website, iOS or Android for an app.

For each step, extract and bank:

- how many screens shipped products needed for this part of the flow
- what the step asks for and, more importantly, what it defers
- where proof, price and commitment appear in the sequence
- what the back and abandon paths do
- which component carries it, so Phase 2 can match it to one the design system already has

Close the tab when the research is done. It is the user's real browser: close only tabs you opened.

### 60fps.design — `https://60fps.design/`

Recorded real-product interactions. Free. The motion and transition source: what happens *between* two screens, how a sheet enters, what a state change looks like.

Use it when the question is about transition, feedback or timing rather than layout. Flow files are static, so bank motion as a sentence in the decision table, not a video link: "the drawer enters from the right with the page dimming behind it, ~250ms, ease-out" survives in the file; a URL does not.

Cross-check against the installed motion skills (`animate`, `css-animations`, `apple-design`) before banking anything that bounces or runs long. House rules still apply: ease-out on entrances, under 300ms for UI motion, no bouncing easings.

## Free fallbacks

No payment, no signup. Use these when the user chose free sources in Phase 0, or said skip at a wall.

| Source | Best for |
|---|---|
| `banani.co` | General app screens; the closest free approximation of Mobbin's browse |
| `mobilepatterns.io` | "How do apps do <function>" |
| `collectui.com` | Single components |
| `land-book.com`, `godly.website` | Landing, pricing, about pages |
| `reallygoodemails.com` | Transactional and confirmation email |
| Apple HIG, Material 3 | Settling a convention argument |

**The known gap:** no free source indexes multi-screen flows. Without Mobbin, step-by-step questions are answered from platform guidelines plus the closest single-screen references, and those rows carry `principle, not reference` so the user knows which decisions are softer.

**Never use Dribbble or Behance.** Concept work nobody had to build looks better than shipped product precisely because nobody had to build it.

## Banking format

Everything goes to `reference-bank.md` in the scratchpad before drawing. One row per step:

```markdown
| Step | Decision | Source | Confidence |
|---|---|---|---|
| 1 of 5 | Carry the date the visitor already chose into the form | Mobbin MCP — Airbnb, Booking.com | reference |
| 2 of 5 | Ask dates before identity; identity last | Mobbin MCP — Zillow, Blueground | reference |
| 4 of 5 | A failed send keeps every field and names one next action | Mobbin MCP — Etsy, Gusto | reference |
| 3 of 5 | The reply-time line shows both clocks | the positioning doc, audience section | principle, not reference |
```

The rows become each board's *Rests on* line and the file's *Why it looks like this* table. `principle, not reference` rows are the likeliest to be wrong; they are named in the Phase 6 report.

## How much to bank

- Up to 5 steps: bank every step, 10–20 minutes of lookups.
- 6–12 steps: bank every step that changes what the user commits to, and every state that is not the happy path; static steps can lean on the design system.
- Over 12 steps: the request is probably several features. Split it with the user first.

Stop when a new lookup stops changing the answer. Three products agreeing on a pattern is a convention; go and look up something else.
