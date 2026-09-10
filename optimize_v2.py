#!/usr/bin/env python3
"""
Round 2 optimization: hero form, FAQ schema, city meta descriptions,
breadcrumb schema, llms.txt
"""
import os, re

ROOT = "/Users/rosey./real-estate-websites/brevardfl"
PHONE = "321-342-2514"
PHONE_TEL = "tel:321-342-2514"
DOMAIN = "https://sellmyhousefastbrevardfl.com"

def read_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ============================================================
# 1. HOMEPAGE: Add hero lead form, FAQ schema, BreadcrumbList
# ============================================================
idx_path = os.path.join(ROOT, "index.html")
content = read_file(idx_path)
orig = content

# Add hero form CSS
hero_form_css = """
        /* Hero with Form */
        .hero-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 50px; align-items: center; text-align: left; }
        .hero-text h1 { font-size: 2.6rem; margin-bottom: 20px; line-height: 1.2; }
        .hero-text p { font-size: 1.2rem; margin-bottom: 25px; opacity: 0.9; }
        .hero-form { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); color: #333; }
        .hero-form h3 { color: #1a365d; margin-bottom: 20px; font-size: 1.3rem; text-align: center; }
        .hero-form .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .hero-form input, .hero-form select { width: 100%; padding: 12px; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 1rem; }
        .hero-form button { width: 100%; padding: 14px; background: #fbbf24; color: #1a365d; border: none; border-radius: 5px; font-weight: bold; font-size: 1.1rem; cursor: pointer; margin-top: 15px; }
        .hero-form button:hover { transform: translateY(-2px); }
        .hero-form p { font-size: 0.85rem; color: #718096; text-align: center; margin-top: 12px; }
        @media (max-width: 768px) {
            .hero-grid { grid-template-columns: 1fr; text-align: center; }
            .hero-form { margin-top: 30px; }
            .hero-form .form-row { grid-template-columns: 1fr; }
        }
"""

if '.hero-grid' not in content:
    content = content.replace(
        '        /* Trust Bar */',
        hero_form_css + '\n        /* Trust Bar */'
    )
    print("Added hero form CSS")

# Replace hero section with split layout + form
old_hero = '''    <!-- Hero -->
    <section class="hero">
        <div class="container">
            <h1>Stop Foreclosure & Settle Estates Fast in Brevard County</h1>
            <p>Cash offers in 24 hours. Close in 10 days or less. No repairs, no fees, no stress — even if you're facing foreclosure or dealing with a loved one's estate.</p>
            <a href="#contact" class="btn">Get Your Cash Offer Now</a>
            <a href="tel:321-342-2514" class="btn btn-secondary">Call 321-342-2514</a>
        </div>
    </section>'''

new_hero = '''    <!-- Hero -->
    <section class="hero">
        <div class="container hero-grid">
            <div class="hero-text">
                <h1>Stop Foreclosure & Settle Estates Fast in Brevard County</h1>
                <p>Cash offers in 24 hours. Close in 10 days or less. No repairs, no fees, no stress — even if you're facing foreclosure or dealing with a loved one's estate.</p>
                <a href="#contact" class="btn">Get Your Cash Offer Now</a>
                <a href="tel:321-342-2514" class="btn btn-secondary">Call 321-342-2514</a>
            </div>
            <div class="hero-form">
                <h3>Get Your Free Cash Offer</h3>
                <form onsubmit="event.preventDefault(); document.getElementById('contact').scrollIntoView({behavior:'smooth'}); document.querySelector('.contact').style.boxShadow='0 0 0 4px #fbbf24'; setTimeout(()=>document.querySelector('.contact').style.boxShadow='',1500);">
                    <div class="form-row">
                        <input type="text" name="full_name" placeholder="Full Name" required>
                        <input type="tel" name="phone" placeholder="Phone Number" required>
                    </div>
                    <input type="text" name="address" placeholder="Property Address" required style="width:100%;padding:12px;border:1px solid #e2e8f0;border-radius:5px;font-size:1rem;margin-top:15px;">
                    <select name="situation" required style="width:100%;padding:12px;border:1px solid #e2e8f0;border-radius:5px;font-size:1rem;margin-top:15px;background:white;">
                        <option value="">Select your situation...</option>
                        <option value="foreclosure">Facing Foreclosure</option>
                        <option value="probate">Probate / Inherited</option>
                        <option value="relocation">Relocation</option>
                        <option value="repairs">Needs Repairs</option>
                        <option value="landlord">Tired Landlord</option>
                        <option value="other">Other</option>
                    </select>
                    <button type="submit">Get My Offer</button>
                </form>
                <p>🔒 Your information is confidential. No spam.</p>
            </div>
        </div>
    </section>'''

if old_hero in content:
    content = content.replace(old_hero, new_hero)
    print("Replaced hero with split layout + form")

# Add FAQPage schema before </head>
faq_schema = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "How fast can you buy my house in Brevard County?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "We can make a fair cash offer within 24 hours of seeing your property. If you accept, we can close in as little as 7-10 days — or on whatever timeline works best for you."
      }}
    }},
    {{
      "@type": "Question",
      "name": "Do I need to make repairs before selling?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "No. We buy houses as-is in any condition. You don't need to clean, repair, or stage anything. We handle all renovations after closing."
      }}
    }},
    {{
      "@type": "Question",
      "name": "Are there any fees or commissions?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Zero. There are no realtor commissions, no closing costs, and no hidden fees. The cash offer we present is exactly what you receive at closing."
      }}
    }},
    {{
      "@type": "Question",
      "name": "Can you help if I'm facing foreclosure?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Yes. We specialize in helping homeowners stop foreclosure in Brevard County. We can close quickly — often before the auction date — so you protect your equity and credit."
      }}
    }},
    {{
      "@type": "Question",
      "name": "What areas in Brevard County do you buy houses?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "We buy houses throughout Brevard County including Melbourne, Palm Bay, Cocoa, Cocoa Beach, Titusville, Rockledge, Merritt Island, Satellite Beach, Viera, Indialantic, Indian Harbour Beach, Melbourne Beach, and Cape Canaveral."
      }}
    }}
  ]
}}
</script>
'''

if 'FAQPage' not in content:
    content = content.replace('</head>', faq_schema + '\n</head>')
    print("Added FAQPage schema to homepage")

# Add BreadcrumbList schema to homepage
breadcrumb_schema = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://sellmyhousefastbrevardfl.com/"
    }}
  ]
}}
</script>
'''

if 'BreadcrumbList' not in content:
    content = content.replace('</head>', breadcrumb_schema + '\n</head>')
    print("Added BreadcrumbList schema to homepage")

if content != orig:
    write_file(idx_path, content)
    print("Saved homepage v2 optimizations")

# ============================================================
# 2. FAQ PAGE: Add BreadcrumbList schema
# ============================================================
faq_path = os.path.join(ROOT, "faq.html")
if os.path.exists(faq_path):
    content = read_file(faq_path)
    if 'BreadcrumbList' not in content:
        breadcrumb = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://sellmyhousefastbrevardfl.com/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "FAQ",
      "item": "https://sellmyhousefastbrevardfl.com/faq"
    }}
  ]
}}
</script>
'''
        content = content.replace('</head>', breadcrumb + '\n</head>')
        write_file(faq_path, content)
        print("Added BreadcrumbList to FAQ page")

# ============================================================
# 3. NICHE PAGES: Add BreadcrumbList schema
# ============================================================
niche_slugs = {
    "avoid-foreclosure-brevard.html": "Avoid Foreclosure",
    "cash-buyer-vs-ibuyer-brevard.html": "Cash Buyer vs iBuyer",
    "cash-home-buyers-brevard.html": "Cash Home Buyers",
    "florida-probate-timeline.html": "Florida Probate Timeline",
    "foreclosure-auction-brevard.html": "Foreclosure Auction",
    "holiday-home-sales-brevard.html": "Holiday Home Sales",
    "inherited-house-brevard.html": "Inherited House",
    "inherited-house-multiple-heirs-florida.html": "Inherited House Multiple Heirs",
    "inherited-property-taxes-florida.html": "Inherited Property Taxes",
    "pre-foreclosure-notice-brevard.html": "Pre-Foreclosure Notice",
    "probate-real-estate-florida.html": "Probate Real Estate",
    "sell-hoarder-house-brevard.html": "Sell Hoarder House",
    "sell-house-as-is-brevard.html": "Sell House As-Is",
    "sell-house-in-foreclosure-brevard.html": "Sell House in Foreclosure",
}

for fname, name in niche_slugs.items():
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        continue
    content = read_file(path)
    if 'BreadcrumbList' in content:
        continue
    slug = fname.replace(".html", "")
    breadcrumb = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://sellmyhousefastbrevardfl.com/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "{name}",
      "item": "https://sellmyhousefastbrevardfl.com/{slug}"
    }}
  ]
}}
</script>
'''
    content = content.replace('</head>', breadcrumb + '\n</head>')
    write_file(path, content)
    print(f"Added BreadcrumbList to {fname}")

# ============================================================
# 4. CITY PAGES: Unique, CTR-optimized meta descriptions
# ============================================================
city_descriptions = {
    "sell-my-house-fast-melbourne.html": "Sell your house fast in Melbourne, FL — Eau Gallie, Suntree, West Melbourne. Cash offer in 24 hrs. No repairs. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-palm-bay.html": "Sell your house fast in Palm Bay, FL — Port Malabar, Bayside Lakes. Fair cash offer in 24 hours. No fees. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-cocoa.html": "Sell your house fast in Cocoa, FL — Cocoa Village, College Manor. Cash buyers. Offer in 24 hrs. No repairs needed. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-cocoa-beach.html": "Sell your house fast in Cocoa Beach, FL — near the pier & cruise port. Cash offer in 24 hrs. No fees. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-titusville.html": "Sell your house fast in Titusville, FL — near Kennedy Space Center. Cash offer in 24 hrs. No repairs. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-satellite-beach.html": "Sell your house fast in Satellite Beach, FL — beachside living. Cash buyers. Offer in 24 hrs. No fees. Close fast. Call 321-342-2514.",
    "sell-my-house-fast-rockledge.html": "Sell your house fast in Rockledge, FL — near Viera & Melbourne. Cash offer in 24 hrs. No repairs. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-merritt-island.html": "Sell your house fast in Merritt Island, FL — near Cocoa Beach & KSC. Cash offer in 24 hrs. No fees. Close fast. Call 321-342-2514.",
    "sell-my-house-fast-viera.html": "Sell your house fast in Viera, FL — The Avenues, Duran Golf Club area. Cash buyers. Offer in 24 hrs. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-indialantic.html": "Sell your house fast in Indialantic, FL — beachside community. Cash offer in 24 hrs. No repairs. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-indian-harbour-beach.html": "Sell your house fast in Indian Harbour Beach, FL. Cash buyers. Fair offer in 24 hrs. No fees. Close in 7 days. Call 321-342-2514.",
    "sell-my-house-fast-melbourne-beach.html": "Sell your house fast in Melbourne Beach, FL — oceanfront & riverfront. Cash offer in 24 hrs. No repairs. Close fast. Call 321-342-2514.",
    "sell-my-house-fast-cape-canaveral.html": "Sell your house fast in Cape Canaveral, FL — near Port Canaveral. Cash buyers. Offer in 24 hrs. Close in 7 days. Call 321-342-2514.",
}

for fname, desc in city_descriptions.items():
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        continue
    content = read_file(path)
    # Find and replace meta description
    old_desc = re.search(r'<meta name="description" content="[^"]*"', content)
    if old_desc:
        old = old_desc.group(0)
        new = f'<meta name="description" content="{desc}"'
        if old != new:
            content = content.replace(old, new)
            write_file(path, content)
            print(f"Updated meta description: {fname}")

# ============================================================
# 5. Create llms.txt
# ============================================================
llms_content = """# Sell My House Fast Brevard FL

We are Brevard Cash Buyers, a cash home buyer serving Brevard County, Florida and the entire Space Coast.

## What We Do
We buy houses in any condition for cash. No repairs needed. No realtor commissions. No closing costs. We can close in as little as 7-10 days, or on your timeline.

## Situations We Help With
- Foreclosure / pre-foreclosure
- Probate and inherited properties
- Tired landlords with problem tenants
- Divorce or separation
- Job relocation
- Houses needing major repairs
- Hoarder houses
- Properties with tax liens or code violations

## Service Area
We buy houses throughout Brevard County, FL including:
Melbourne, Palm Bay, Cocoa, Cocoa Beach, Titusville, Rockledge, Merritt Island, Satellite Beach, Viera, Indialantic, Indian Harbour Beach, Melbourne Beach, Cape Canaveral.

## How It Works
1. Contact us with your property address and situation
2. We research the property and present a fair cash offer within 24 hours
3. Close on your timeline — as fast as 7 days, or whenever you're ready

## Contact
Phone: 321-342-2514
Email: info@sellmyhousefastbrevardfl.com
Website: https://sellmyhousefastbrevardfl.com

## About Us
- 5-star rated by homeowners across Brevard County
- Local market experts who know Melbourne, Palm Bay, Cocoa, and every Space Coast community
- No obligation offers — you decide if our price works for you
- Transparent process with no hidden fees
"""

llms_path = os.path.join(ROOT, "llms.txt")
with open(llms_path, "w", encoding="utf-8") as f:
    f.write(llms_content)
print("Created llms.txt")

print("All v2 optimizations complete.")
