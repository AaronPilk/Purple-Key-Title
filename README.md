# Purple Key Title &amp; Escrow

Marketing site for Purple Key Title &amp; Escrow — a **South Carolina only** title agency,
underwritten by **WFG National Title Insurance Company**.

Static HTML/CSS/JS, generated from a config-driven Python script. No framework, no build
step at deploy time — the generated files are committed and served as-is.

---

## Repo layout

```
build.py              generator — SITE config, all page copy, page templates
prepare_assets.py     image pipeline — crops/grades/exports WebP + JPEG at each width
src/style.css         stylesheet source  → copied to assets/style.css by build.py
src/main.js           script source      → copied to assets/main.js by build.py
assets/img/           logo, icons, OG card, responsive photography
*.html                generated pages (committed)
sitemap.xml robots.txt site.webmanifest  generated
```

## Rebuild

```bash
python3 build.py
```

Edit copy and structure in `build.py`, styles in `src/style.css`, behaviour in
`src/main.js`. Never edit the generated `*.html` or `assets/style.css` directly —
the next build overwrites them.

Re-export imagery only if the source frames change:

```bash
python3 prepare_assets.py ~/path/to/image-library assets/img
```

## Deployment

Cloudflare Pages, connected to this repo:

| Setting            | Value    |
| ------------------ | -------- |
| Framework preset   | None     |
| Build command      | *(empty)* |
| Output directory   | `/`      |
| Production branch  | `main`   |

Pushes to `main` deploy automatically.

---

## Before launch — items awaiting client sign-off

These live in the `SITE` dict at the top of `build.py`. Set the value, run
`python3 build.py`, commit. Every link, footer line and schema block reads from there.

- [ ] **Phone number** — `SITE["phone"]`. Currently empty, which renders
      "Phone number coming soon" on the contact page and in the footer, and omits
      `telephone` from the structured data. Set it to e.g. `"(843) 555-0100"` and every
      `tel:` link builds itself.
- [ ] **Confirm the orders email** — `SITE["email"]` is set to `orders@purplekeytitle.com`
      on the assumption it follows the domain. Confirm before launch; it is the
      destination for every Order Title and Contact action on the site.
- [ ] **Confirm the domain** — `SITE["url"]` drives canonicals, the sitemap and OG tags.
- [ ] **Physical / mailing address** — deliberately absent. The spec says not to publish
      one unless the company confirms it should be public.
- [ ] **Business hours** — omitted for the same reason.
- [ ] **Approved WFG logo asset** — the underwriter is referenced in text only. The spec
      permits the WFG logo *only* if an approved asset is supplied.
- [ ] **Horizontal logo lockup** — the supplied mark is a tall, detailed crest. It is used
      exactly as approved, at a generous size, in a deliberately spacious header. A
      horizontal crest-plus-wordmark lockup would let the header shrink without the
      wordmark becoming unreadable. The spec asks that an alternate be *requested*
      rather than cropped, so it has not been cropped.
- [ ] **Legal review of `privacy.html` and `terms.html`** — written for this site rather
      than copied from a sibling, but not reviewed by counsel.
- [ ] **Social links** — none published yet.

## Guardrails baked into this build

Straight from the client specification. Worth re-reading before editing copy.

- **South Carolina only.** North Carolina is not referenced anywhere. This site is the
  exception to the sibling sites' Carolinas-wide coverage.
- **WFG is the only underwriter** named anywhere — copy, footer, metadata, alt text, links.
- **No rate calculator**, fee calculator or external underwriter tool. Not added by default.
- **No forms.** Order Title opens a pre-structured email; Contact is call/email actions.
  No Social Security numbers, bank details or wire instructions are ever requested.
- **No invented facts** — no founding date, years in business, awards, transaction volume,
  team size, office count or ownership claims.
- **No speed promises** — no "24/7", "nights and weekends", "one-hour", no guaranteed clear
  title and no guaranteed closing dates.
- **Not a law firm.** South Carolina requires a licensed South Carolina attorney to
  supervise a real estate closing; the copy says Purple Key *coordinates with* the closing
  attorney and does not give legal advice.
- **No city anchoring.** South Carolina is the service area; no city is featured.
- **Restraint over ornament.** The logo carries the crown, key and palmetto — those
  symbols are not repeated through the sections, and purple is used as a premium accent
  rather than a gradient wash.
