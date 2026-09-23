# Purple Key Title LLC

Marketing site for Purple Key Title LLC — a **South Carolina only** title agency,
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

## Client revision round 2 — applied 22 Sep 2026

From *Purple Key Title FINAL Website Revision Requests*:

- Phone **704-627-3031** wired through the footer, Contact page, click-to-call links
  and structured data. The "coming soon" placeholder is gone.
- Order Title mailto now prefills the subject **"New Title Order - Purple Key Title."**
- Benefit card **"WFG-Backed Protection" → "National Underwriter Strength"**, with WFG
  still named in the supporting line.
- Service-area heading → **"Serving South Carolina statewide."** on both the homepage and
  the Contact page, with the region list reordered so it no longer leads with the coast.
- **Photography repositioned** away from coastal/tropical toward Rock Hill / Fort Mill /
  Midlands / Upstate character. Replaced: the tropical hero, the dated About image with the
  visible older vehicle, the coastal cottage, and the palm-shadow detail shot. The process
  image was kept, as requested. No palms, no beach, no dated vehicles remain.
- Header logo enlarged (104px in a 132px header; 70px on mobile) so the crest and tagline
  stay legible.
- Process step numbering hardened — one badge per step, list markers suppressed on the
  `<ol>` and each `<li>`.

## Client revision round 3 — applied 23 Sep 2026

From *Exact Remaining Website Revisions*:

- **Legal company name is `Purple Key Title LLC`.** Renamed across every visible string,
  title tag, meta description, Open Graph tag, JSON-LD schema, footer copyright, legal
  pages and image alt text — 123 references. `Purple Key Title & Escrow` appears nowhere.
- **The escrow *service* was deliberately left intact** — her note says removing "Escrow"
  from the company name does not remove the service. "Escrow & Transaction Support" and
  `escrow-transaction-support.html` are unchanged.
- Hero eyebrow changed from "South Carolina Title & Escrow" to "South Carolina Title
  Services" so the line above the headline no longer echoes the old company name.
  **Flagged for her** — it is the one copy line changed that she did not explicitly list.
- Service-area supporting sentence replaced with her exact wording.
- **Process step numbering**: the `<ol>`/`<li>` markup was removed entirely in favour of
  `<div role="list">` / `<div role="listitem">`. A browser list-marker can no longer render
  a second number beside the badge — there is now only one number-producing mechanism in
  both the source and the render. Verified on rendered desktop (1440px) and mobile (390px).
- OG card caption corrected to "South Carolina Title Insurance".

### Known blocker — corrected logo asset

The supplied logo artwork reads **"PURPLE KEY / TITLE & ESCROW"**, which is not the legal
company name. Her instruction is explicit: *"Replace it with an approved corrected logo…
Do not crop, distort, or cover the existing logo wording as a workaround."*

No corrected asset has been supplied, so the original logo is still in place, unaltered.
Drop the revised file in as `purplekeytitle logo.png` and re-run:

```bash
python3 prepare_assets.py ~/mnt/higgsfieldimages assets/img   # only if imagery changed
python3 build.py
```

…then regenerate the favicons and OG card from the new artwork. Until then, the header,
footer and social card all still show the old wordmark.

### Imagery update 23 Sep 2026 (round 3b)

The hero and About images were both refined brick colonials and read as near-duplicates of
each other. Her own About brief asks for "a second image that complements the hero but is
not a duplicate", so both were replaced:

| Slot  | Was                         | Now                                                        |
| ----- | --------------------------- | ---------------------------------------------------------- |
| hero  | brick Georgian (idx 182)    | stone + timber transitional home at dusk (idx 56)           |
| about | brick colonial (idx 70)     | white farmhouse on rolling pasture, golden hour (idx 69)    |

Neither red brick colonial is used anywhere on the site now. Both replacements sit inside
her stated palette — "refined brick, stone, painted brick, traditional or transitional
Southern home, tasteful landscaping, mature hardwoods".

**Worth her eye:** the new hero is the most contemporary image on the site and it is shot at
blue hour rather than bright daylight. It is explicitly permitted by the brief ("stone…
transitional Southern home") but if she wants brighter and more traditional, index 7
(painted stucco and timber on an established street, full daylight) is the ready alternative
— change `"hero"` in `prepare_assets.py` to `idx=7` and re-run.

### Note on her round-3 image feedback

Items 2 and 3 of her list asked for the hero and About images to be replaced because they
"still" showed palms and Spanish moss. Those were replaced on 22 Sep; the live assets were
verified as the brick Georgian and the brick colonial with a magnolia. She was reviewing a
cached copy of the page. A hard refresh (Cmd+Shift+R) shows the current images.

## Client image swap — 23 Sep 2026 (round 4)

Two approved files supplied by the client, used exactly as delivered:

| Slot    | File                                          | Handling                                   |
| ------- | --------------------------------------------- | ------------------------------------------ |
| hero    | `twilight_modern_farmhouse_elegance.png`      | native 16:9, no crop, no grade             |
| process | `modern_title_insurance_office_dashboard.png` | 4:3 → 3:2, cropped from the bottom only    |

Originals live in `assets/source/`. `prepare_assets.py` now takes a `file=` path as well as
a library `idx=`, and a `raw=True` slot skips the house colour grade — client-approved
artwork ships exactly as supplied.

The process crop takes height off the bottom only (`fy=0.00`). The brief said not to crop
away the professional, the monitor or the coverage content on screen, and the subject's head
already touches the top edge of the source, so any top crop would clip it. 3:2 rather than
16:9 keeps the desk items intact too.

**Image URLs are now cache-busted.** Every `assets/img/*` URL carries `?v=<content hash>`.
Filenames are unchanged, so nothing else had to move, but a changed image always gets a new
URL. This was added because the client twice reviewed a cached page and reported images as
unchanged when they had already been replaced.

### Open question for the client — the office/dashboard image

Worth raising before launch. It is on the site as instructed, but:

1. It shows a **Purple Key client portal that does not exist**. On the site it implies the
   company offers a customer-facing coverage dashboard. The original brief was explicit
   about not advertising things the company does not have.
2. It carries a **second, conflicting logo and tagline** — a house mark reading
   "PURPLE KEY TITLE · PEOPLE PROPERTY POSSIBILITIES" — which is not the approved crest and
   not "Unlocking Legacy. Securing Tomorrows." Two brand marks now appear on one page. If
   this house mark is the corrected logo the brief asked for, the real file is still needed.
3. The wall art, mug and notebook carry invented slogans. Earlier rounds barred fabricated
   signage in imagery.

None of this blocks the build; it is a client decision.

## Still open before launch

- [ ] **Confirm the domain** — `SITE["url"]` drives canonicals, the sitemap and OG tags.
      Currently `purplekeytitle.com`; no custom domain is attached to the deployment yet.
- [ ] **Physical / mailing address** — deliberately absent. The client's instruction is not
      to publish one unless specifically approved later.
- [ ] **Business hours** — omitted for the same reason.
- [ ] **Approved WFG logo asset** — the underwriter is referenced in text only. The spec
      permits the WFG logo *only* if an approved asset is supplied.
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
