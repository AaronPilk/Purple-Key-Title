#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Purple Key Title LLC - static site generator.

Everything that changes between builds lives in SITE and the copy blocks below.
Run `python3 build.py` from the repo root; pages are written to the root so
Cloudflare Pages can serve with output directory "/".
"""
import json
import math
import os
import re
import shutil
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# SITE
# ---------------------------------------------------------------------------
SITE = {
    "name": "Purple Key Title LLC",
    "short": "Purple Key Title",
    "domain": "purplekeytitle.com",
    "url": "https://purplekeytitle.com",
    "email": "orders@purplekeytitle.com",
    # Confirmed by the client 22 Sep 2026. Every tel: link, footer line and
    # schema block below reads from here.
    "phone": "704-627-3031",
    "phone_display": "704-627-3031",
    "region": "South Carolina",
    "region_abbr": "SC",
    "underwriter": "WFG National Title Insurance Company",
    "underwriter_short": "WFG",
    "tagline": "Unlocking Legacy. Securing Tomorrows.",
    "year": 2026,
}

ORDER_BODY = """Please open a new title order.

Contact name:
Company / firm:
Email:
Phone:
Property address:
County:
Transaction type (Purchase / Refinance / Cash / Commercial / Land / Other):
Role (Buyer / Seller / Realtor / Lender / Investor / Attorney / Other):
Requested service:
Target closing date:
Notes / special instructions:

For your security, please do not send Social Security numbers, bank account
numbers, wire instructions or other sensitive financial details by email.
"""

ORDER_HREF = "mailto:%s?subject=%s&body=%s" % (
    SITE["email"],
    urllib.parse.quote("New Title Order - Purple Key Title."),
    urllib.parse.quote(ORDER_BODY),
)
ASK_HREF = "mailto:%s?subject=%s" % (SITE["email"], urllib.parse.quote("Question for Purple Key Title LLC"))


def tel_href():
    digits = re.sub(r"\D", "", SITE["phone"])
    return "tel:+1" + digits if digits else ""


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "residential-title-insurance",
        "nav": "Residential Title Insurance",
        "short": "Residential",
        "img": "residential",
        "card_sub": "Protection for the place you call home.",
        "card_desc": "Thorough title work and dependable title insurance designed to protect "
                     "homebuyers and lenders from covered title risks.",
        "h1": "Protecting the place you call home.",
        "lede": "Buying a home is a major investment. Purple Key provides thorough title review and "
                "dependable title insurance designed to help protect ownership and reduce the risk of "
                "covered title problems after closing. We work closely with the professionals involved "
                "in the transaction to help keep the process clear, organized, and moving forward.",
        "alt": "A newly built two-storey home with stone and lap siding on a quiet residential "
               "street",
        "included": [
            ("Title search and examination",
             "A review of the public record for ownership history, liens, judgments, easements, "
             "restrictions and other matters that can affect the property."),
            ("Title commitment",
             "A clear written summary of what the policy will cover and what has to be resolved before "
             "the policy can be issued."),
            ("Requirement clearance",
             "Coordination with the parties who can address payoffs, releases, estate matters and "
             "similar items identified in the search."),
            ("Owner's and lender's policies",
             "Policies underwritten by %s, issued after closing and the completion of applicable "
             "requirements." % SITE["underwriter"]),
        ],
        "for_who": "First-time buyers, move-up buyers, homeowners refinancing, and the lenders and real "
                   "estate professionals working alongside them.",
    },
    {
        "slug": "investor-title-services",
        "nav": "Investor Title Services",
        "short": "Investors",
        "img": "investors",
        "card_sub": "Protection that grows with your portfolio.",
        "card_desc": "Responsive title support for individual acquisitions, repeat investors, and "
                     "growing real estate portfolios.",
        "h1": "A dependable title partner for your next acquisition.",
        "lede": "Whether you are purchasing one investment property or building a growing portfolio, "
                "Purple Key provides responsive title support designed for repeat transactions, changing "
                "timelines, and investment-focused needs. Our goal is to help identify title issues early, "
                "protect ownership, and keep acquisitions moving efficiently.",
        "alt": "An aerial view of an established South Carolina neighborhood of traditional homes "
               "under mature trees",
        "included": [
            ("Repeat-file handling",
             "A consistent point of contact and a consistent process across multiple files, so each new "
             "order does not start from scratch."),
            ("Early issue identification",
             "Searches read with an eye toward the matters that most often delay investor purchases - "
             "unreleased mortgages, judgments, tax items and heirs' property questions."),
            ("Entity and vesting review",
             "Attention to how title is being taken, so the documents match the way the investment is "
             "actually held."),
            ("Portfolio and multi-parcel orders",
             "Coordination across several properties in one transaction, with requirements tracked "
             "parcel by parcel."),
        ],
        "for_who": "Individual investors, repeat buyers, rental portfolio owners, 1031 participants, and "
                   "the lenders financing them.",
    },
    {
        "slug": "land-title",
        "nav": "Land Title",
        "short": "Land",
        "img": "land",
        "card_sub": "Clarity before you build.",
        "card_desc": "Careful title review for vacant land, acreage, development property, and other "
                     "land transactions.",
        "h1": "Clarity before you build.",
        "lede": "Land transactions can involve unique title considerations, access questions, easements, "
                "restrictions, prior ownership issues, and development concerns. Purple Key provides "
                "careful title review and dependable title insurance for vacant land, acreage, and "
                "development property throughout South Carolina.",
        "alt": "Rolling Upstate South Carolina pasture at sunrise with a split-rail fence and a dirt "
               "track running toward the treeline",
        "included": [
            ("Access and easement review",
             "A look at recorded access, rights of way and easements that affect how the parcel can be "
             "reached and used."),
            ("Boundary and legal description review",
             "Attention to how the parcel is described in the record and whether that description is "
             "consistent across prior conveyances."),
            ("Restrictions and covenants",
             "Identification of recorded restrictions, covenants and reservations that may affect "
             "development plans."),
            ("Heirs' property and long chains",
             "Careful handling of the older, longer chains of title that rural and family-held land "
             "often carries."),
        ],
        "for_who": "Land buyers, builders, developers, timber and farm owners, and lenders financing "
                   "acreage.",
    },
    {
        "slug": "commercial-title-insurance",
        "nav": "Commercial Title Insurance",
        "short": "Commercial",
        "img": "commercial",
        "card_sub": "Protection built for higher-stakes transactions.",
        "card_desc": "Experienced title support for commercial acquisitions, financing, ownership "
                     "structures, and complex property matters.",
        "h1": "Protection built for higher-stakes transactions.",
        "lede": "Commercial real estate often involves significant investment, complex ownership "
                "structures, financing requirements, and greater transaction risk. Purple Key provides "
                "thorough title review and dependable title insurance designed to protect the investment, "
                "reduce risk, and provide confidence from acquisition forward.",
        "alt": "A stone and glass commercial office building on a South Carolina corner at golden hour, "
               "framed by mature oaks",
        "included": [
            ("Entity and authority review",
             "Review of the organizational documents and authority needed for the entity on title to "
             "convey or encumber the property."),
            ("Survey and ALTA matters",
             "Coordination around survey review and the endorsements a commercial lender or buyer "
             "commonly requires."),
            ("Multi-party coordination",
             "Working with counsel, lenders, brokers and the other parties a commercial file brings to "
             "the table."),
            ("Endorsement support",
             "Requests for available endorsements handled with %s so coverage matches the deal."
             % SITE["underwriter_short"]),
        ],
        "for_who": "Commercial buyers and sellers, developers, landlords, lenders and the attorneys "
                   "representing them.",
    },
    {
        "slug": "escrow-transaction-support",
        "nav": "Escrow & Transaction Support",
        "short": "Escrow",
        "img": "escrow",
        "card_sub": "Details handled with care.",
        "card_desc": "Responsive coordination and transaction support designed to keep documents, "
                     "requirements, and communication moving efficiently.",
        "h1": "Details handled. Transactions moving.",
        "lede": "Purple Key provides responsive escrow and transaction support designed to keep "
                "requirements, documentation, and transaction details organized from the day the order "
                "is opened through policy issuance.",
        "alt": "A fountain pen resting on cream paper beside reading glasses and a brass desk lamp",
        "included": [
            ("Order intake and file setup",
             "Getting the property, parties and timeline into the file accurately at the start, so "
             "nothing has to be chased later."),
            ("Document coordination",
             "Gathering payoffs, releases, affidavits and the other items a file needs, and tracking "
             "what is still outstanding."),
            ("Status communication",
             "Straightforward updates to the parties who need them, without having to ask twice."),
            ("Policy issuance",
             "Issuing the appropriate title insurance policy after closing and completion of applicable "
             "requirements."),
        ],
        "for_who": "Everyone on the file - buyers, sellers, agents, lenders and the closing attorney.",
        "note": "South Carolina requires that a licensed South Carolina attorney supervise a real estate "
                "closing. Purple Key is a title agency, not a law firm, and does not provide legal advice "
                "or conduct closings independently. We coordinate with the closing attorney and the other "
                "transaction parties.",
    },
]

BENEFITS = [
    ("Clear Communication", "Straightforward updates and responsive answers throughout the transaction."),
    ("Thorough Review", "Careful attention to title details, requirements, and potential issues."),
    ("Responsive Service", "A team focused on keeping the transaction moving without sacrificing accuracy."),
    ("South Carolina Focus", "Title services focused exclusively on properties and transactions in South Carolina."),
    ("Residential to Commercial", "Support for homebuyers, investors, land transactions, lenders, and commercial clients."),
    ("National Underwriter Strength",
     "Local service supported by the resources and financial strength of %s."
     % SITE["underwriter"]),
]

PROCESS = [
    ("Submit the order", "Send the property and transaction information through the Order Title link."),
    ("Title search &amp; review", "The title is researched and reviewed for ownership, liens, restrictions, "
                                  "and other matters that may affect the transaction."),
    ("Clear requirements &amp; coordinate", "Work with the appropriate parties to address title requirements "
                                            "and prepare the transaction for closing."),
    ("Policy issuance", "After closing and completion of applicable requirements, issue the appropriate "
                        "title insurance policy."),
]

FAQS = [
    ("What does title insurance actually protect against?",
     "A title insurance policy protects against covered problems in the property's recorded history that "
     "were not discovered before closing - things like an unreleased mortgage, an unpaid lien, a "
     "defective prior deed, an undisclosed heir, or a recording error. It is different from homeowners "
     "insurance, which covers future damage to the property itself."),
    ("What is the difference between an owner's policy and a lender's policy?",
     "A lender's policy protects the lender's interest in the property, up to the loan amount, and is "
     "generally required when there is a mortgage. An owner's policy protects the buyer's own interest "
     "in the property. A lender's policy does not protect the owner."),
    ("Do I still need title insurance if I am paying cash?",
     "A lender's policy will not apply, because there is no lender. An owner's policy is the one that "
     "protects the buyer, and a cash purchase does not reduce the risk that something in the property's "
     "recorded history could surface later."),
    ("What happens during a title search?",
     "The public record for the property is examined - deeds, mortgages, judgments, tax records, plats, "
     "estate files and similar sources - to establish the chain of ownership and identify anything "
     "recorded against the property that has to be addressed before closing."),
    ("What is a title commitment?",
     "The commitment is the written document issued before closing that sets out what the policy will "
     "cover, who has to sign, what has to be paid or released, and what the policy will not cover. It is "
     "worth reading, and we are happy to walk through it."),
    ("Does South Carolina require an attorney at closing?",
     "Yes. South Carolina requires that a licensed South Carolina attorney supervise a real estate "
     "closing. Purple Key is a title agency rather than a law firm; we handle the title search, "
     "examination, requirement clearance and title insurance, and we coordinate with the closing attorney "
     "and the other parties to the transaction."),
    ("Who chooses the title company?",
     "In most transactions the buyer or the party paying for the policy has the right to choose. If you "
     "would like Purple Key on the file, the request can be made in the contract or passed along to your "
     "agent, lender or closing attorney."),
    ("How long does title work take?",
     "It depends on the county where the property sits, the type of property, the length of the chain of "
     "title, and what the search turns up. Older parcels, estate files, heirs' property and land "
     "transactions generally take longer than a recent subdivision resale. We will tell you what we are "
     "waiting on rather than leaving you to guess."),
    ("What are the most common title problems?",
     "Unreleased mortgages and liens, unpaid property or income taxes, judgments against a prior owner, "
     "boundary and easement questions, errors in a prior legal description, and unresolved estate or "
     "heirship matters."),
    ("What do you need to open a file?",
     "The property address and county, the parties to the transaction, the contract or loan information, "
     "and a contact for each side. Send what you have through the Order Title link and we will follow up "
     "on anything missing."),
]

# ---------------------------------------------------------------------------
# South Carolina outline, drawn from boundary coordinates rather than traced art
# ---------------------------------------------------------------------------
SC_COORDS = [
    (-83.10, 34.99), (-83.00, 35.03), (-82.78, 35.08), (-82.55, 35.16), (-82.36, 35.20),
    (-82.22, 35.19), (-81.95, 35.19), (-81.50, 35.18), (-81.36, 35.16), (-81.04, 35.15),
    (-81.04, 35.10), (-80.93, 35.10), (-80.84, 35.00), (-80.80, 34.94), (-80.56, 34.82),
    (-80.32, 34.82), (-79.92, 34.81), (-79.68, 34.80), (-79.45, 34.62), (-79.19, 34.40),
    (-78.99, 33.95), (-78.65, 33.83), (-78.90, 33.69), (-79.09, 33.44), (-79.29, 33.22),
    (-79.55, 33.05), (-79.85, 32.86), (-79.93, 32.72), (-80.19, 32.57), (-80.45, 32.50),
    (-80.67, 32.38), (-80.80, 32.22), (-80.88, 32.03), (-81.09, 32.08), (-81.15, 32.30),
    (-81.40, 32.60), (-81.55, 32.90), (-81.85, 33.25), (-81.97, 33.47), (-82.20, 33.70),
    (-82.45, 34.05), (-82.70, 34.30), (-82.85, 34.50), (-83.00, 34.72),
]


def sc_path(width=520.0, pad=6.0):
    lat0 = math.radians(sum(p[1] for p in SC_COORDS) / len(SC_COORDS))
    pts = [(lon * math.cos(lat0), lat) for lon, lat in SC_COORDS]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    sx = (width - pad * 2) / (max(xs) - min(xs))
    out = []
    for x, y in pts:
        out.append(((x - min(xs)) * sx + pad, (max(ys) - y) * sx + pad))
    height = (max(ys) - min(ys)) * sx + pad * 2
    d = "M " + " L ".join("%.1f %.1f" % p for p in out) + " Z"
    return d, width, height


SC_D, SC_W, SC_H = sc_path()

# ---------------------------------------------------------------------------
# Markup helpers
# ---------------------------------------------------------------------------
NAV_PRIMARY = [("index.html", "Home"), ("about.html", "About")]
NAV_TAIL = [("resources.html", "Resources"), ("contact.html", "Contact")]


def logo_size(path="assets/img/logo-512.png", fallback=(463, 512)):
    """Intrinsic dimensions for the logo <img>, read from the approved file so
    the reserved box always matches and nothing shifts on load."""
    try:
        from PIL import Image
        with Image.open(os.path.join(ROOT, path)) as im:
            return im.size
    except Exception:
        return fallback


LOGO_W, LOGO_H = logo_size()


def picture(slot, widths, sizes, alt, cls="", w=None, h=None, eager=False, ratio=None):
    widths = sorted(widths)
    big = widths[-1]
    if ratio and not (w and h):
        w, h = big, int(round(big * ratio[1] / ratio[0]))
    webp = ", ".join("assets/img/%s-%d.webp %dw" % (slot, x, x) for x in widths)
    jpg = ", ".join("assets/img/%s-%d.jpg %dw" % (slot, x, x) for x in widths)
    loading = "" if eager else ' loading="lazy" decoding="async"'
    fetch = ' fetchpriority="high"' if eager else ""
    return (
        '<picture class="%s">'
        '<source type="image/webp" srcset="%s" sizes="%s">'
        '<img src="assets/img/%s-%d.jpg" srcset="%s" sizes="%s" alt="%s" width="%d" height="%d"%s%s>'
        "</picture>" % (cls, webp, sizes, slot, big, jpg, sizes, alt, w, h, loading, fetch)
    )


def head(title, desc, canonical, extra=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s/%s">
<meta name="theme-color" content="#FBFAF7">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s/%s">
<meta property="og:image" content="%s/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.ico" sizes="any">
<link rel="icon" href="assets/img/icon-32.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/icon-180.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/style.css">
%s</head>
<body>
<a class="skip" href="#main">Skip to content</a>
""" % (title, desc, SITE["url"], canonical, SITE["name"], title, desc, SITE["url"], canonical,
       SITE["url"], extra)


def header(active=""):
    def link(href, label):
        cur = ' aria-current="page"' if href == active else ""
        return '<a href="%s"%s>%s</a>' % (href, cur, label)

    svc_open = ' class="open"' if active.replace(".html", "") in [s["slug"] for s in SERVICES] or active == "services.html" else ""
    svc_items = "".join(
        '<a href="%s.html" role="menuitem"><span class="dd-t">%s</span>'
        '<span class="dd-d">%s</span></a>' % (s["slug"], s["nav"], s["card_sub"])
        for s in SERVICES
    )
    primary = "".join(link(h, l) for h, l in NAV_PRIMARY)
    tail = "".join(link(h, l) for h, l in NAV_TAIL)
    mob = "".join('<a href="%s">%s</a>' % (h, l) for h, l in NAV_PRIMARY)
    mob += '<a href="services.html">Services</a>'
    mob += "".join('<a class="sub" href="%s.html">%s</a>' % (s["slug"], s["nav"]) for s in SERVICES)
    mob += "".join('<a href="%s">%s</a>' % (h, l) for h, l in NAV_TAIL)

    return """<header class="site-head" id="head">
  <div class="wrap head-in">
    <a class="brand" href="index.html" aria-label="%(name)s - home">
      <img src="assets/img/logo-512.png" alt="%(name)s" width="%(lw)d" height="%(lh)d">
    </a>
    <nav class="nav" aria-label="Primary">
      %(primary)s
      <div class="has-dd%(svc_open)s">
        <button class="dd-btn" aria-expanded="false" aria-haspopup="true">Services<svg viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></button>
        <div class="dd" role="menu">
          <a href="services.html" role="menuitem" class="dd-all"><span class="dd-t">All title services</span><span class="dd-d">An overview of everything Purple Key handles.</span></a>
          %(svc_items)s
        </div>
      </div>
      %(tail)s
    </nav>
    <a class="btn btn-p head-cta" href="%(order)s">Order Title</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
  </div>
  <div class="mobile" hidden>
    <nav aria-label="Mobile">%(mob)s</nav>
    <a class="btn btn-p btn-block" href="%(order)s">Order Title</a>
  </div>
</header>
""" % dict(name=SITE["name"], primary=primary, tail=tail, svc_items=svc_items, mob=mob,
           order=ORDER_HREF, svc_open=svc_open, lw=LOGO_W, lh=LOGO_H)


def cta_band():
    return """<section class="band-cta reveal">
  <div class="wrap narrow center">
    <p class="eyebrow on-dark">Get started</p>
    <h2 class="h-xl on-dark">Ready to unlock a smoother title experience?</h2>
    <p class="lede on-dark">Whether you are buying a home, investing in property, financing a
      transaction, or helping a client close, Purple Key is ready to help protect what comes next.</p>
    <div class="btns center-btns">
      <a class="btn btn-light" href="%s">Order Title</a>
      <a class="btn btn-ghost-light" href="contact.html">Contact Us</a>
    </div>
  </div>
</section>
""" % ORDER_HREF


def footer():
    phone_line = ""
    if SITE["phone"]:
        phone_line = '<a href="%s">%s</a>' % (tel_href(), SITE["phone"])
    else:
        phone_line = '<span class="muted">%s</span>' % SITE["phone_display"]
    svc_links = "".join('<a href="%s.html">%s</a>' % (s["slug"], s["nav"]) for s in SERVICES)
    return """<footer class="site-foot">
  <div class="wrap foot-in">
    <div class="foot-brand">
      <img src="assets/img/logo-512.png" alt="%(name)s" width="%(lw)d" height="%(lh)d" loading="lazy">
      <p class="foot-line">Title insurance and title services throughout South Carolina.</p>
      <p class="foot-tag">%(tagline)s</p>
    </div>
    <div class="foot-cols">
      <div><h3>Services</h3>%(svc)s</div>
      <div><h3>Company</h3>
        <a href="about.html">About</a>
        <a href="services.html">All Services</a>
        <a href="resources.html">Resources &amp; FAQ</a>
        <a href="contact.html">Contact</a>
      </div>
      <div><h3>Get in touch</h3>
        <a href="%(order)s">Order Title</a>
        <a href="mailto:%(email)s">%(email)s</a>
        %(phone)s
      </div>
    </div>
  </div>
  <div class="wrap foot-bar">
    <p>&copy; %(year)d %(name)s. All rights reserved.</p>
    <p class="foot-uw">Authorized title insurance agent of %(uw)s.</p>
    <p class="foot-legal"><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms</a></p>
  </div>
</footer>
<script src="assets/main.js" defer></script>
</body>
</html>
""" % dict(name=SITE["name"], tagline=SITE["tagline"], svc=svc_links, order=ORDER_HREF,
           email=SITE["email"], phone=phone_line, year=SITE["year"], uw=SITE["underwriter"],
           lw=LOGO_W, lh=LOGO_H)


def schema():
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": SITE["name"],
        "description": "Title insurance and title services for residential, investor, land and "
                       "commercial transactions throughout South Carolina.",
        "url": SITE["url"],
        "logo": SITE["url"] + "/assets/img/logo-512.png",
        "image": SITE["url"] + "/assets/img/og.jpg",
        "email": SITE["email"],
        "areaServed": {"@type": "State", "name": "South Carolina"},
        "serviceType": [s["nav"] for s in SERVICES],
    }
    if SITE["phone"]:
        data["telephone"] = SITE["phone"]
    return '<script type="application/ld+json">%s</script>\n' % json.dumps(data)


def faq_schema():
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS
        ],
    }
    return '<script type="application/ld+json">%s</script>\n' % json.dumps(data)


def page_hero(eyebrow, h1, lede, small=True):
    return """<section class="page-hero%s">
  <div class="wrap">
    <p class="eyebrow">%s</p>
    <h1 class="h-xl">%s</h1>
    <p class="lede">%s</p>
  </div>
</section>
""" % (" tight" if small else "", eyebrow, h1, lede)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def build_index():
    cards = ""
    for s in SERVICES:
        cards += """    <a class="svc-card reveal" href="%s.html">
      %s
      <div class="svc-body">
        <h3>%s</h3>
        <p class="svc-sub">%s</p>
        <p>%s</p>
        <span class="arrow">Learn more<svg viewBox="0 0 16 12" aria-hidden="true"><path d="M9.5 1L15 6l-5.5 5M15 6H1" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      </div>
    </a>
""" % (s["slug"],
       picture(s["img"], [600, 800, 1200], "(max-width: 700px) 92vw, (max-width: 1080px) 46vw, 30vw",
               s["alt"], cls="svc-img", ratio=(3, 2)),
       s["nav"], s["card_sub"], s["card_desc"])

    benefits = ""
    for t, d in BENEFITS:
        benefits += """      <div class="benefit reveal">
        <span class="arc" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10.6" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="12" cy="12" r="2.5" fill="currentColor"/></svg></span>
        <h3>%s</h3><p>%s</p>
      </div>
""" % (t, d)

    steps = ""
    for i, (t, d) in enumerate(PROCESS, 1):
        steps += """      <div class="step reveal" role="listitem"><span class="step-n">%d</span>
        <h3>%s</h3><p>%s</p></div>
""" % (i, t, d)

    body = head(
        "Purple Key Title LLC | South Carolina Title Insurance",
        "Purple Key Title LLC provides title insurance and title services for homebuyers, "
        "investors, lenders, land, and commercial transactions throughout South Carolina.",
        "", schema())
    body += header("index.html")
    body += """<main id="main">

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">South Carolina Title Services</p>
    <h1 class="h-hero">The key to confident ownership.</h1>
    <p class="lede">Purple Key Title LLC provides thorough title services, dependable title
      insurance, and responsive transaction support for homebuyers, investors, lenders, and real estate
      professionals across South Carolina. Backed by %(uw)s, we combine careful review, clear
      communication, and experienced service to help protect ownership and keep transactions moving.</p>
    <div class="btns">
      <a class="btn btn-p" href="%(order)s">Order Title</a>
      <a class="btn btn-o" href="services.html">Explore Our Services</a>
    </div>
  </div>
  <div class="wrap hero-media">
    %(heroimg)s
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="split-media reveal">%(aboutimg)s</div>
    <div class="split-copy reveal">
      <p class="eyebrow">Who we are</p>
      <h2 class="h-xl">A title partner built around trust.</h2>
      <p>Purple Key Title LLC was created to make title protection feel clear, responsive, and
        personal. We bring careful title review, dependable communication, and close attention to every
        detail so buyers, investors, lenders, and real estate professionals can move forward with
        confidence.</p>
      <a class="arrow link" href="about.html">More about Purple Key<svg viewBox="0 0 16 12" aria-hidden="true"><path d="M9.5 1L15 6l-5.5 5M15 6H1" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h2 class="h-xl">The right title services for every transaction.</h2>
    <p class="lede">From residential purchases and land transactions to investment properties, escrow
      support, and complex commercial deals, Purple Key provides dependable title services designed to
      protect ownership, reduce risk, and keep transactions moving.</p>
  </div>
  <div class="wrap svc-grid">
%(cards)s  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow">Why Purple Key</p>
    <h2 class="h-xl">The key difference is in the details.</h2>
    <p class="lede">Title protection is only part of the experience. Purple Key is built around
      responsive communication, careful work, and dependable service at every stage of the
      transaction.</p>
  </div>
  <div class="wrap benefits">
%(benefits)s  </div>
</section>

<section class="sec band uw">
  <div class="wrap narrow center">
    <p class="eyebrow">Underwriter</p>
    <h2 class="h-lg">Local service. National strength.</h2>
    <span class="rule" aria-hidden="true"></span>
    <p class="lede">Purple Key Title LLC is an authorized title insurance agent of %(uw)s,
      combining responsive local service with the resources and financial strength of a national
      underwriter.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow">The process</p>
    <h2 class="h-xl">From order to policy, made clear.</h2>
  </div>
  <div class="wrap proc-media reveal">%(processimg)s</div>
  <div class="wrap">
    <div class="steps-row" role="list">
%(steps)s    </div>
  </div>
</section>

<section class="sec band">
  <div class="wrap coverage">
    <div class="cov-copy reveal">
      <p class="eyebrow">Service area</p>
      <h2 class="h-xl">Serving South Carolina statewide.</h2>
      <p class="lede">Purple Key provides title services for properties and transactions throughout
        South Carolina, with responsive service and the same careful attention to every file - wherever
        the transaction takes place.</p>
      <div class="btns">
        <a class="btn btn-p" href="%(order)s">Order Title</a>
        <a class="btn btn-o" href="contact.html">Contact Our Team</a>
      </div>
    </div>
    <div class="cov-map reveal" aria-hidden="true">
      <svg viewBox="0 0 %(scw).0f %(sch).0f" role="img" aria-label="Outline of the state of South Carolina">
        <path d="%(scd)s" class="sc-fill"/>
        <path d="%(scd)s" class="sc-line"/>
      </svg>
      <p class="cov-cap">Serving South Carolina</p>
    </div>
  </div>
</section>

</main>
""" % dict(uw=SITE["underwriter"], order=ORDER_HREF, cards=cards, benefits=benefits, steps=steps,
           scd=SC_D, scw=SC_W, sch=SC_H,
           heroimg=picture("hero", [800, 1200, 1800],
                           "(max-width: 1240px) 94vw, 1200px",
                           "A brick South Carolina home with white columns, azaleas in bloom and "
                           "mature oaks along a circular drive", cls="hero-img", ratio=(16, 9), eager=True),
           aboutimg=picture("about", [600, 900, 1400],
                            "(max-width: 900px) 92vw, 46vw",
                            "A red brick home framed by mature oaks and a magnolia, with azaleas along "
                            "the front beds", cls="rounded", ratio=(4, 3)),
           processimg=picture("process", [700, 1000, 1600],
                              "(max-width: 1240px) 94vw, 1200px",
                              "Architectural drawings laid out on a walnut table with stone, wood and "
                              "tile samples", cls="proc-img", ratio=(16, 9)))
    body += cta_band() + footer()
    return body


def build_about():
    body = head(
        "About | Purple Key Title LLC",
        "Purple Key Title LLC helps South Carolina property owners and real estate "
        "professionals move forward with greater clarity and confidence.",
        "about.html", schema())
    body += header("about.html")
    body += """<main id="main">
%(hero)s
  <div class="wrap hero-media">%(img)s</div>

<section class="sec">
  <div class="wrap split">
    <div class="split-copy reveal">
      <p class="eyebrow">Brand story</p>
      <h2 class="h-xl">Protection for today. Confidence for what comes next.</h2>
      <p>A property can represent a home, an investment, a business opportunity, or a legacy for the
        future. Purple Key approaches every file with the care those goals deserve - protecting
        ownership, identifying title risks, and helping the people behind the transaction move forward
        with confidence.</p>
      <p class="tagline-quote">%(tagline)s</p>
    </div>
    <div class="split-media reveal">%(detail)s</div>
  </div>
</section>

<section class="sec band">
  <div class="wrap">
    <p class="eyebrow">How we work</p>
    <h2 class="h-xl">The key difference is in the details.</h2>
    <p class="lede">Title protection is only part of the experience. Purple Key is built around
      responsive communication, careful work, and dependable service at every stage of the
      transaction.</p>
  </div>
  <div class="wrap benefits">
%(benefits)s  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow">Underwriter</p>
    <h2 class="h-lg">Local service. National strength.</h2>
    <p class="lede">Purple Key Title LLC is an authorized title insurance agent of %(uw)s,
      combining responsive local service with the resources and financial strength of a national
      underwriter.</p>
    <p class="fine">Purple Key Title LLC is a title agency. It is not a law firm and does not
      provide legal advice. South Carolina requires that a licensed South Carolina attorney supervise a
      real estate closing; we coordinate with the closing attorney and the other parties to the
      transaction.</p>
  </div>
</section>
</main>
""" % dict(hero=page_hero("About Purple Key", "Unlocking confidence in every transaction.",
                          "Purple Key Title LLC is focused on one thing: helping South Carolina "
                          "property owners and real estate professionals move forward with greater "
                          "clarity and confidence. We combine attentive service, thorough title work, and "
                          "dependable title insurance protection with a commitment to making every "
                          "transaction feel organized, responsive, and well cared for.", small=False),
           img=picture("colonial", [600, 800, 1200], "(max-width: 1240px) 94vw, 1200px",
                       "A traditional craftsman home with a deep front porch, stone columns and "
                       "azaleas in an established South Carolina neighborhood",
                       cls="hero-img", ratio=(3, 2)),
           detail=picture("detail", [600, 900], "(max-width: 900px) 92vw, 42vw",
                          "Antique brass hardware on white oak cabinetry beside a marble countertop",
                          cls="rounded", ratio=(3, 4)),
           benefits="".join(
               '      <div class="benefit reveal"><span class="arc" aria-hidden="true">'
               '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10.6" fill="none" stroke="currentColor" '
               'stroke-width="1"/><circle cx="12" cy="12" r="2.5" fill="currentColor"/></svg></span>'
               '<h3>%s</h3><p>%s</p></div>\n' % (t, d) for t, d in BENEFITS),
           uw=SITE["underwriter"], tagline=SITE["tagline"])
    body += cta_band() + footer()
    return body


def build_services():
    cards = ""
    for s in SERVICES:
        cards += """    <a class="svc-card reveal" href="%s.html">
      %s
      <div class="svc-body">
        <h3>%s</h3>
        <p class="svc-sub">%s</p>
        <p>%s</p>
        <span class="arrow">Learn more<svg viewBox="0 0 16 12" aria-hidden="true"><path d="M9.5 1L15 6l-5.5 5M15 6H1" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      </div>
    </a>
""" % (s["slug"],
       picture(s["img"], [600, 800, 1200], "(max-width: 700px) 92vw, (max-width: 1080px) 46vw, 30vw",
               s["alt"], cls="svc-img", ratio=(3, 2)),
       s["nav"], s["card_sub"], s["card_desc"])

    body = head("Title Services in South Carolina | Purple Key Title LLC",
                "Residential, investor, land, commercial title insurance and escrow support for "
                "transactions throughout South Carolina.",
                "services.html", schema())
    body += header("services.html")
    body += """<main id="main">
%s
  <div class="wrap svc-grid top">
%s  </div>

<section class="sec band">
  <div class="wrap narrow center">
    <p class="eyebrow">Underwriter</p>
    <h2 class="h-lg">Local service. National strength.</h2>
    <span class="rule" aria-hidden="true"></span>
    <p class="lede">Every Purple Key policy is underwritten by %s, combining responsive local service
      with the resources and financial strength of a national underwriter.</p>
  </div>
</section>
</main>
""" % (page_hero("Our services", "The right title services for every transaction.",
                 "From residential purchases and land transactions to investment properties, escrow "
                 "support, and complex commercial deals, Purple Key provides dependable title services "
                 "designed to protect ownership, reduce risk, and keep transactions moving.", small=False),
       cards, SITE["underwriter"])
    body += cta_band() + footer()
    return body


def build_service(s):
    others = [x for x in SERVICES if x["slug"] != s["slug"]]
    incl = "".join(
        '      <div class="incl reveal"><h3>%s</h3><p>%s</p></div>\n' % (t, d) for t, d in s["included"])
    rel = "".join(
        '      <a class="rel-card" href="%s.html"><span class="rel-t">%s</span>'
        '<span class="rel-d">%s</span></a>\n' % (o["slug"], o["nav"], o["card_sub"]) for o in others)
    note = ""
    if s.get("note"):
        note = '  <div class="wrap"><p class="fine">%s</p></div>\n' % s["note"]

    body = head("%s in South Carolina | %s" % (s["nav"], SITE["name"]),
                s["card_desc"], "%s.html" % s["slug"], schema())
    body += header("%s.html" % s["slug"])
    body += """<main id="main">
%(hero)s
  <div class="wrap hero-media">%(img)s</div>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow">What is included</p>
    <h2 class="h-xl">%(sub)s</h2>
  </div>
  <div class="wrap incl-grid">
%(incl)s  </div>
</section>

<section class="sec band">
  <div class="wrap">
    <p class="eyebrow">Who it is for</p>
    <h2 class="h-lg">Built for the people on the file.</h2>
    <p class="lede">%(for_who)s</p>
%(note)s  </div>
</section>

<section class="sec">
  <div class="wrap"><p class="eyebrow">Also from Purple Key</p><h2 class="h-lg">Other title services</h2></div>
  <div class="wrap rel-grid">
%(rel)s  </div>
</section>
</main>
""" % dict(hero=page_hero(s["nav"], s["h1"], s["lede"], small=False),
           img=picture(s["img"], [600, 800, 1200], "(max-width: 1240px) 94vw, 1200px",
                       s["alt"], cls="hero-img", ratio=(3, 2)),
           sub=s["card_sub"], incl=incl, for_who=s["for_who"], rel=rel, note=note)
    body += cta_band() + footer()
    return body


def build_resources():
    items = ""
    for i, (q, a) in enumerate(FAQS):
        items += """      <details class="faq"%s>
        <summary><span>%s</span><span class="chev" aria-hidden="true"><svg viewBox="0 0 12 8"><path d="M1 1l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></span></summary>
        <div class="faq-a"><p>%s</p></div>
      </details>
""" % (" open" if i == 0 else "", q, a)

    body = head("Title Insurance Resources &amp; FAQ | Purple Key Title LLC",
                "Straight answers about title insurance, title searches, escrow and the South Carolina "
                "closing process.",
                "resources.html", schema() + faq_schema())
    body += header("resources.html")
    body += """<main id="main">
%s
<section class="sec">
  <div class="wrap">
    <div class="faq-wrap">
%s    </div>
  </div>
</section>

<section class="sec band">
  <div class="wrap narrow center">
    <h2 class="h-lg">Still have a question?</h2>
    <p class="lede">Send it over and we will give you a straight answer.</p>
    <div class="btns center-btns">
      <a class="btn btn-p" href="%s">Email our team</a>
      <a class="btn btn-o" href="%s">Order Title</a>
    </div>
  </div>
</section>
</main>
""" % (page_hero("Resources", "Title, explained plainly.",
                 "Title insurance has its own vocabulary. Here is what the terms actually mean and what "
                 "to expect from a South Carolina transaction - without the jargon.", small=False),
       items, ASK_HREF, ORDER_HREF)
    body += cta_band() + footer()
    return body


def build_contact():
    phone_card = ""
    if SITE["phone"]:
        phone_card = """      <a class="act reveal" href="%s">
        <span class="act-e">Call</span>
        <span class="act-t">%s</span>
        <span class="act-d">Speak with the team directly.</span>
      </a>
""" % (tel_href(), SITE["phone"])
    else:
        phone_card = """      <div class="act act-soon reveal">
        <span class="act-e">Call</span>
        <span class="act-t">%s</span>
        <span class="act-d">Until then, email is the fastest way to reach us.</span>
      </div>
""" % SITE["phone_display"]

    body = head("Contact | Purple Key Title LLC",
                "Reach Purple Key Title LLC to open a title order or ask a question about a "
                "South Carolina transaction.",
                "contact.html", schema())
    body += header("contact.html")
    body += """<main id="main">
%(hero)s
<section class="sec tight-top">
  <div class="wrap acts">
      <a class="act act-primary reveal" href="%(order)s">
        <span class="act-e">Order Title</span>
        <span class="act-t">Open a new file</span>
        <span class="act-d">Opens an email with everything we need - property, county, parties and
          timeline - already laid out.</span>
      </a>
      <a class="act reveal" href="%(ask)s">
        <span class="act-e">Email</span>
        <span class="act-t">%(email)s</span>
        <span class="act-d">Questions about a file, a commitment or a closing.</span>
      </a>
%(phone)s  </div>
  <div class="wrap">
    <p class="fine">For your security, please do not send Social Security numbers, bank account numbers,
      wire instructions or other sensitive financial details by email. Wire instructions are never
      changed by email - always verify payment details by phone with a number you already know.</p>
  </div>
</section>

<section class="sec band">
  <div class="wrap split">
    <div class="split-media reveal">%(img)s</div>
    <div class="split-copy reveal">
      <p class="eyebrow">Service area</p>
      <h2 class="h-xl">Serving South Carolina statewide.</h2>
      <p>Purple Key provides title services for properties and transactions throughout South
        Carolina, with responsive service and the same careful attention to every file - wherever the
        transaction takes place. Send the address and county and we will take it from there.</p>
      <p class="fine">Purple Key Title LLC is a title agency, not a law firm, and does not
        provide legal advice. South Carolina requires that a licensed South Carolina attorney supervise a
        real estate closing.</p>
    </div>
  </div>
</section>
</main>
""" % dict(hero=page_hero("Contact", "Let's get the file started.",
                          "Order a title, ask a question, or check on a file in progress. Purple Key "
                          "responds to every message that comes in.", small=False),
           order=ORDER_HREF, ask=ASK_HREF, email=SITE["email"], phone=phone_card,
           img=picture("contact", [800, 1200], "(max-width: 900px) 92vw, 46vw",
                       "A magnolia blossom, fountain pen and cup of tea on a light oak desk",
                       cls="rounded", ratio=(3, 2)))
    body += cta_band() + footer()
    return body


LEGAL_PRIVACY = [
    ("What this policy covers",
     "This policy explains how Purple Key Title LLC handles information collected through this "
     "website. It does not describe how information is handled inside an active title or escrow file; "
     "that is governed by the agreements and disclosures provided with the transaction."),
    ("Information collected through this site",
     "This website does not use contact forms and does not ask visitors to submit personal information "
     "through the site. When you choose to email or call us using the links provided, you decide what to "
     "send, and that message reaches us the same way any other email or phone call does."),
    ("What we ask you not to send",
     "Please do not send Social Security numbers, bank account or card numbers, wire instructions, "
     "passwords, or other sensitive financial details by email. If we need information of that kind, we "
     "will tell you how to provide it securely."),
    ("Analytics and cookies",
     "This site does not set advertising cookies and does not sell visitor information. If analytics are "
     "added in the future, this policy will be updated to say what is collected and why."),
    ("Third-party services",
     "Web fonts are loaded from Google Fonts, which receives the request needed to deliver the font "
     "files. Site hosting is provided by our hosting vendor, which keeps standard server logs."),
    ("Questions",
     "Questions about this policy can be sent to %s." % SITE["email"]),
]

LEGAL_TERMS = [
    ("Informational purposes",
     "The content on this website is provided for general information only. It is not legal advice, tax "
     "advice, or a commitment to insure any particular property or transaction."),
    ("Not a law firm",
     "Purple Key Title LLC is a title insurance agency. It is not a law firm and does not "
     "provide legal advice or representation. South Carolina requires that a licensed South Carolina "
     "attorney supervise a real estate closing, and we coordinate with the closing attorney and the "
     "other parties to the transaction."),
    ("Coverage is governed by the policy",
     "Title insurance coverage is determined solely by the terms, conditions and exclusions of the "
     "issued policy and by the commitment that precedes it. Nothing on this website expands, alters or "
     "guarantees coverage, clear title, or any closing date."),
    ("Service area",
     "Purple Key Title LLC provides title services for properties and transactions in South "
     "Carolina."),
    ("Underwriter",
     "Purple Key Title LLC is an authorized title insurance agent of %s. References to the "
     "underwriter on this site describe that agency relationship and nothing more."
     % SITE["underwriter"]),
    ("Changes",
     "These terms may be updated from time to time. Continued use of the site follows the version "
     "posted here."),
]


def build_legal(title, eyebrow, h1, lede, blocks, canonical):
    secs = "".join(
        '    <div class="legal-block"><h2>%s</h2><p>%s</p></div>\n' % (h, b) for h, b in blocks)
    body = head("%s | %s" % (title, SITE["name"]), lede, canonical, schema())
    body += header(canonical)
    body += """<main id="main">
%s
<section class="sec tight-top">
  <div class="wrap">
    <div class="legal">
%s      <p class="fine">Last updated September 2026.</p>
    </div>
  </div>
</section>
</main>
""" % (page_hero(eyebrow, h1, lede, small=False), secs)
    body += footer()
    return body


def build_404():
    body = head("Page not found | %s" % SITE["name"],
                "That page could not be found.", "404.html")
    body += header()
    body += """<main id="main">
<section class="page-hero">
  <div class="wrap narrow center">
    <p class="eyebrow">404</p>
    <h1 class="h-xl">That page has moved on.</h1>
    <p class="lede">The link may be out of date. Everything Purple Key offers is one step away.</p>
    <div class="btns center-btns">
      <a class="btn btn-p" href="index.html">Back to home</a>
      <a class="btn btn-o" href="services.html">Our services</a>
    </div>
  </div>
</section>
</main>
"""
    body += footer()
    return body


# ---------------------------------------------------------------------------
CSS = open(os.path.join(ROOT, "src", "style.css")).read() if os.path.exists(
    os.path.join(ROOT, "src", "style.css")) else ""
JS = open(os.path.join(ROOT, "src", "main.js")).read() if os.path.exists(
    os.path.join(ROOT, "src", "main.js")) else ""

MANIFEST = json.dumps({
    "name": SITE["name"],
    "short_name": SITE["short"],
    "start_url": "/",
    "display": "standalone",
    "background_color": "#FBFAF7",
    "theme_color": "#470F55",
    "icons": [
        {"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
    ],
}, indent=2)


def main():
    pages = {
        "index.html": build_index(),
        "about.html": build_about(),
        "services.html": build_services(),
        "resources.html": build_resources(),
        "contact.html": build_contact(),
        "404.html": build_404(),
        "privacy.html": build_legal(
            "Privacy Policy", "Legal", "Privacy Policy",
            "How Purple Key Title LLC handles information in connection with this website.",
            LEGAL_PRIVACY, "privacy.html"),
        "terms.html": build_legal(
            "Terms", "Legal", "Terms of Use",
            "The terms that apply to this website and the information published on it.",
            LEGAL_TERMS, "terms.html"),
    }
    for s in SERVICES:
        pages["%s.html" % s["slug"]] = build_service(s)

    for name, html in pages.items():
        with open(os.path.join(ROOT, name), "w") as fh:
            fh.write(html)

    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    if CSS:
        with open(os.path.join(ROOT, "assets", "style.css"), "w") as fh:
            fh.write(CSS)
    if JS:
        with open(os.path.join(ROOT, "assets", "main.js"), "w") as fh:
            fh.write(JS)
    with open(os.path.join(ROOT, "site.webmanifest"), "w") as fh:
        fh.write(MANIFEST)

    urls = ["", "about.html", "services.html", "resources.html", "contact.html",
            "privacy.html", "terms.html"] + ["%s.html" % s["slug"] for s in SERVICES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>%s/%s</loc><changefreq>monthly</changefreq>"
                  "<priority>%s</priority></url>" % (SITE["url"], u, "1.0" if u == "" else "0.7"))
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as fh:
        fh.write("\n".join(sm) + "\n")

    with open(os.path.join(ROOT, "robots.txt"), "w") as fh:
        fh.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["url"])

    print("built %d pages" % len(pages))
    for n in sorted(pages):
        print("  ", n)


if __name__ == "__main__":
    main()
