#!/usr/bin/env python3
"""
Conversion optimization script for Brevard website.
Fixes: 4xx errors, duplicate content, missing schema, missing internal links,
inconsistent phone numbers, adds trust signals.
"""
import os, re, json

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
# 1. Fix /cities/ 4xx in breadcrumb schema on city pages
# ============================================================
city_pages = [f for f in os.listdir(ROOT) if f.startswith("sell-my-house-fast-") and f.endswith(".html")]
for fname in city_pages:
    path = os.path.join(ROOT, fname)
    content = read_file(path)
    # Remove the "Cities We Serve" breadcrumb item that points to /cities/
    old_pattern = r'''\{\s*"@type":\s*"ListItem",\s*"position":\s*2,\s*"name":\s*"Cities We Serve",\s*"item":\s*"https://sellmyhousefastbrevardfl\.com/cities/"\s*\},?'''
    content = re.sub(old_pattern, '', content, flags=re.DOTALL)
    # Fix position numbers if we removed position 2
    content = content.replace('"position": 3,', '"position": 2,')
    write_file(path, content)
    print(f"Fixed breadcrumb: {fname}")

# ============================================================
# 2. Fix duplicate titles on preview/backup pages
# ============================================================
# homepage-live.html -> add noindex and distinct title
hl_path = os.path.join(ROOT, "homepage-live.html")
if os.path.exists(hl_path):
    content = read_file(hl_path)
    if "<title>" in content:
        content = content.replace(
            "<title>Stop Foreclosure & Sell Inherited Property | Brevard County</title>",
            "<title>Homepage Backup | Brevard Cash Buyers</title>"
        )
    if "name=\"robots\"" not in content:
        content = content.replace(
            "<meta name=\"viewport\"",
            '<meta name="robots" content="noindex, nofollow">\n    <meta name="viewport"'
        )
    write_file(hl_path, content)
    print("Fixed homepage-live.html (noindex, distinct title)")

# privacy-preview.html -> noindex, distinct title
pp_path = os.path.join(ROOT, "privacy-preview.html")
if os.path.exists(pp_path):
    content = read_file(pp_path)
    if "<title>" in content:
        content = content.replace(
            "<title>Privacy Policy | Sell My House Fast Brevard FL</title>",
            "<title>Privacy Policy Preview | Brevard Cash Buyers</title>"
        )
    if "name=\"robots\"" not in content:
        content = content.replace(
            "<meta name=\"viewport\"",
            '<meta name="robots" content="noindex, nofollow">\n    <meta name="viewport"'
        )
    write_file(pp_path, content)
    print("Fixed privacy-preview.html (noindex, distinct title)")

# terms-preview.html -> noindex, distinct title
tp_path = os.path.join(ROOT, "terms-preview.html")
if os.path.exists(tp_path):
    content = read_file(tp_path)
    if "<title>" in content:
        content = content.replace(
            "<title>Terms & Conditions | Sell My House Fast Brevard FL</title>",
            "<title>Terms Preview | Brevard Cash Buyers</title>"
        )
    if "name=\"robots\"" not in content:
        content = content.replace(
            "<meta name=\"viewport\"",
            '<meta name="robots" content="noindex, nofollow">\n    <meta name="viewport"'
        )
    write_file(tp_path, content)
    print("Fixed terms-preview.html (noindex, distinct title)")

# ============================================================
# 3. Standardize phone tel: links across all HTML files
# ============================================================
for root, dirs, files in os.walk(ROOT):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        path = os.path.join(root, fname)
        content = read_file(path)
        orig = content
        # Fix tel:3213422514 -> tel:321-342-2514
        content = re.sub(r'href=["\']tel:3213422514["\']', f'href="{PHONE_TEL}"', content)
        if content != orig:
            write_file(path, content)
            rel = os.path.relpath(path, ROOT)
            print(f"Standardized phone links: {rel}")

# ============================================================
# 4. Add schema, canonical, favicon, and internal links to orphaned niche pages
# ============================================================
orphaned_niche = [
    "avoid-foreclosure-brevard.html",
    "cash-buyer-vs-ibuyer-brevard.html",
    "cash-home-buyers-brevard.html",
    "florida-probate-timeline.html",
    "foreclosure-auction-brevard.html",
    "holiday-home-sales-brevard.html",
    "inherited-house-brevard.html",
    "inherited-house-multiple-heirs-florida.html",
    "inherited-property-taxes-florida.html",
    "pre-foreclosure-notice-brevard.html",
    "probate-real-estate-florida.html",
    "sell-hoarder-house-brevard.html",
    "sell-house-as-is-brevard.html",
    "sell-house-in-foreclosure-brevard.html",
]

NAV_HTML = '''<nav style="background:#1a365d;padding:15px 0;position:sticky;top:0;z-index:100;">
  <div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:10px;">
      <img src="/logo-homepage.png" alt="Brevard Cash Buyers" style="height:40px;width:auto;">
      <span style="font-size:1.3rem;font-weight:bold;color:white;">Brevard Cash Buyers</span>
    </div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;">
      <a href="/" style="color:white;text-decoration:none;font-size:0.9rem;">Home</a>
      <a href="/stop-foreclosure-brevard" style="color:white;text-decoration:none;font-size:0.9rem;">Stop Foreclosure</a>
      <a href="/sell-inherited-house-florida" style="color:white;text-decoration:none;font-size:0.9rem;">Inherited House</a>
      <a href="/how-much-do-cash-buyers-pay" style="color:white;text-decoration:none;font-size:0.9rem;">Pricing</a>
      <a href="/testimonials" style="color:white;text-decoration:none;font-size:0.9rem;">Reviews</a>
      <a href="/faq" style="color:white;text-decoration:none;font-size:0.9rem;">FAQ</a>
      <a href="/blog/" style="color:white;text-decoration:none;font-size:0.9rem;">Blog</a>
    </div>
    <div><a href="tel:321-342-2514" style="color:#fbbf24;text-decoration:none;font-weight:600;">321-342-2514</a></div>
  </div>
</nav>
'''

FOOTER_HTML = '''
<footer style="background:#1a365d;color:white;padding:40px 20px;text-align:center;margin-top:40px;">
  <p style="margin-bottom:15px;"><strong>We Buy Houses Throughout Brevard County</strong></p>
  <p style="font-size:0.85rem;line-height:1.8;margin-bottom:15px;">
    <a href="/sell-my-house-fast-melbourne" style="color:white;text-decoration:none;">Melbourne</a> •
    <a href="/sell-my-house-fast-palm-bay" style="color:white;text-decoration:none;">Palm Bay</a> •
    <a href="/sell-my-house-fast-cocoa-beach" style="color:white;text-decoration:none;">Cocoa Beach</a> •
    <a href="/sell-my-house-fast-titusville" style="color:white;text-decoration:none;">Titusville</a> •
    <a href="/sell-my-house-fast-satellite-beach" style="color:white;text-decoration:none;">Satellite Beach</a> •
    <a href="/sell-my-house-fast-indialantic" style="color:white;text-decoration:none;">Indialantic</a> •
    <a href="/sell-my-house-fast-rockledge" style="color:white;text-decoration:none;">Rockledge</a> •
    <a href="/sell-my-house-fast-cocoa" style="color:white;text-decoration:none;">Cocoa</a> •
    <a href="/sell-my-house-fast-merritt-island" style="color:white;text-decoration:none;">Merritt Island</a> •
    <a href="/sell-my-house-fast-viera" style="color:white;text-decoration:none;">Viera</a> •
    <a href="/sell-my-house-fast-indian-harbour-beach" style="color:white;text-decoration:none;">Indian Harbour Beach</a> •
    <a href="/sell-my-house-fast-melbourne-beach" style="color:white;text-decoration:none;">Melbourne Beach</a> •
    <a href="/sell-my-house-fast-cape-canaveral" style="color:white;text-decoration:none;">Cape Canaveral</a>
  </p>
  <p style="font-size:0.85rem;opacity:0.7;">© 2026 Brevard Cash Buyers. Call/Text: <a href="tel:321-342-2514" style="color:#fbbf24;text-decoration:none;">321-342-2514</a></p>
</footer>
'''

RELATED_SECTION = '''
<div style="max-width:720px;margin:40px auto;padding:0 20px;">
  <h2 style="font-size:22px;font-weight:600;margin-top:36px;margin-bottom:16px;color:#1a1a1a;border-bottom:2px solid #ff9f0a;padding-bottom:8px;">Related Articles</h2>
  <ul style="margin-bottom:16px;padding-left:24px;">
    <li style="margin-bottom:8px;"><a href="/stop-foreclosure-brevard" style="color:#2c5282;text-decoration:none;">Stop Foreclosure in Brevard County</a></li>
    <li style="margin-bottom:8px;"><a href="/sell-inherited-house-florida" style="color:#2c5282;text-decoration:none;">Sell an Inherited House in Florida</a></li>
    <li style="margin-bottom:8px;"><a href="/how-much-do-cash-buyers-pay" style="color:#2c5282;text-decoration:none;">How Much Do Cash Buyers Pay?</a></li>
    <li style="margin-bottom:8px;"><a href="/faq" style="color:#2c5282;text-decoration:none;">Frequently Asked Questions</a></li>
  </ul>
</div>
'''

SCHEMA_LOCALBUSINESS = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Brevard Cash Buyers",
  "url": "{url}",
  "telephone": "+1-321-342-2514",
  "email": "info@sellmyhousefastbrevardfl.com",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "Melbourne",
    "addressRegion": "FL",
    "addressCountry": "US"
  }},
  "areaServed": {{
    "@type": "State",
    "name": "Florida"
  }},
  "serviceType": ["Cash Home Buying", "Fast House Sales", "As-Is Home Sales"],
  "priceRange": "$$",
  "openingHours": "Mo-Su 08:00-20:00"
}}
</script>
'''

for fname in orphaned_niche:
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        continue
    content = read_file(path)
    orig = content

    # Add canonical if missing
    if 'rel="canonical"' not in content:
        slug = fname.replace(".html", "")
        canon = f'<link rel="canonical" href="{DOMAIN}/{slug}">\n'
        content = content.replace('<meta name="description"', canon + '<meta name="description"')

    # Replace SVG favicon with real favicon
    if 'favicon.png' not in content:
        content = re.sub(
            r'<link rel="icon" href="data:image/svg[^"]+">',
            '<link rel="icon" type="image/png" href="/favicon.png" sizes="48x48">',
            content
        )

    # Add schema before </head> if missing
    if 'schema.org' not in content:
        slug = fname.replace(".html", "")
        schema = SCHEMA_LOCALBUSINESS.format(url=f"{DOMAIN}/{slug}")
        content = content.replace('</head>', schema + '\n</head>')

    # Add nav after <body> if missing
    if '<nav' not in content and '<header' not in content:
        content = content.replace('<body>', '<body>\n' + NAV_HTML)

    # Add footer before </body> if missing
    if '<footer' not in content:
        # Insert related articles before footer
        content = content.replace('</body>', RELATED_SECTION + FOOTER_HTML + '\n</body>')
    else:
        # If footer exists but no related articles, add them before footer
        if 'Related Articles' not in content:
            content = content.replace('<footer', RELATED_SECTION + '<footer')

    if content != orig:
        write_file(path, content)
        print(f"Enhanced orphaned page: {fname}")

print("Done with orphaned niche pages.")

# ============================================================
# 5. Homepage conversion optimization
# ============================================================
idx_path = os.path.join(ROOT, "index.html")
content = read_file(idx_path)
orig = content

# Add exit-intent modal CSS and JS before </body>
exit_modal = '''
<!-- Exit Intent Modal -->
<div id="exitModal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:999;justify-content:center;align-items:center;">
  <div style="background:white;padding:40px;border-radius:10px;max-width:500px;width:90%;text-align:center;position:relative;">
    <span onclick="document.getElementById('exitModal').style.display='none'" style="position:absolute;top:10px;right:15px;font-size:28px;cursor:pointer;color:#666;">&times;</span>
    <h3 style="color:#1a365d;margin-bottom:15px;font-size:1.5rem;">Wait! Get Your No-Obligation Cash Offer</h3>
    <p style="margin-bottom:20px;color:#4a5568;">Before you go — get a fair cash offer on your Brevard County home in 24 hours. No repairs, no fees.</p>
    <a href="tel:321-342-2514" style="display:inline-block;background:#fbbf24;color:#1a365d;padding:15px 40px;text-decoration:none;border-radius:5px;font-weight:bold;font-size:1.1rem;">Call 321-342-2514</a>
    <p style="margin-top:15px;font-size:0.9rem;"><a href="#contact" onclick="document.getElementById('exitModal').style.display='none'" style="color:#2c5282;">Or fill out the form below →</a></p>
  </div>
</div>
<script>
(function(){
  var shown = false;
  document.addEventListener('mouseout', function(e){
    if(!shown && e.clientY < 10 && !e.relatedTarget){
      shown = true;
      document.getElementById('exitModal').style.display='flex';
    }
  });
  document.getElementById('exitModal').addEventListener('click', function(e){
    if(e.target === this) this.style.display='none';
  });
})();
</script>
'''

if 'exitModal' not in content:
    content = content.replace('</body>', exit_modal + '\n</body>')
    print("Added exit-intent modal to homepage")

# Add testimonials section before CTA section if missing
testimonials_section = '''
    <!-- Testimonials -->
    <section style="padding:80px 0;background:#f7fafc;">
        <div class="container">
            <h2 class="section-title" style="margin-bottom:40px;">Trusted by Brevard County Homeowners</h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:30px;">
                <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:30px;box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                    <div style="font-size:1.2rem;color:#fbbf24;margin-bottom:15px;">⭐⭐⭐⭐⭐</div>
                    <p style="font-style:italic;color:#4a5568;margin-bottom:20px;">"Martin and his team were great to work with. He kept me informed during the entire process and promptly answered any questions."</p>
                    <div style="font-weight:600;color:#1a365d;">Kathy B.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:30px;box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                    <div style="font-size:1.2rem;color:#fbbf24;margin-bottom:15px;">⭐⭐⭐⭐⭐</div>
                    <p style="font-style:italic;color:#4a5568;margin-bottom:20px;">"They were very honest and transparent through the whole process and made selling my house easy. I highly recommend!"</p>
                    <div style="font-weight:600;color:#1a365d;">Collin C.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:30px;box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                    <div style="font-size:1.2rem;color:#fbbf24;margin-bottom:15px;">⭐⭐⭐⭐⭐</div>
                    <p style="font-style:italic;color:#4a5568;margin-bottom:20px;">"Martin was a pleasure to work with! He had a quick solution for our house we had been trying to sell for such a long time."</p>
                    <div style="font-weight:600;color:#1a365d;">Dominic F.</div>
                </div>
            </div>
            <div style="text-align:center;margin-top:30px;">
                <a href="/testimonials" style="color:#2c5282;text-decoration:none;font-weight:600;">Read all 6 reviews →</a>
            </div>
        </div>
    </section>
'''

if 'Trusted by Brevard County Homeowners' not in content:
    content = content.replace(
        '    <!-- CTA Section -->',
        testimonials_section + '\n    <!-- CTA Section -->'
    )
    print("Added testimonials section to homepage")

# Add urgency line to CTA section
if 'Spots fill fast' not in content:
    content = content.replace(
        '    <p>Foreclosure looming? Dealing with probate? Inherited a house you don\'t want? Let\'s talk.</p>',
        '    <p>Foreclosure looming? Dealing with probate? Inherited a house you don\'t want? Let\'s talk.</p>\n            <p style="font-weight:600;margin-top:15px;font-size:1.1rem;">🔥 We buy 5-7 houses per month in Brevard County. Spots fill fast — call today.</p>'
    )
    print("Added urgency line to homepage CTA")

# Add Review/AggregateRating schema to homepage if missing
if '"aggregateRating"' not in content or '"review"' not in content:
    review_schema = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Brevard Cash Buyers",
  "url": "https://sellmyhousefastbrevardfl.com",
  "telephone": "+1-321-342-2514",
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "6",
    "bestRating": "5",
    "worstRating": "1"
  }},
  "review": [
    {{
      "@type": "Review",
      "author": {{ "@type": "Person", "name": "Kathy B." }},
      "reviewBody": "Martin and his team were great to work with. He kept me informed during the entire process and promptly answered any questions.",
      "reviewRating": {{ "@type": "Rating", "ratingValue": "5", "bestRating": "5" }}
    }},
    {{
      "@type": "Review",
      "author": {{ "@type": "Person", "name": "Collin C." }},
      "reviewBody": "They were very honest and transparent through the whole process and made selling my house easy. I highly recommend!",
      "reviewRating": {{ "@type": "Rating", "ratingValue": "5", "bestRating": "5" }}
    }}
  ]
}}
</script>
'''
    content = content.replace('</head>', review_schema + '</head>')
    print("Added review schema to homepage")

if content != orig:
    write_file(idx_path, content)
    print("Saved homepage optimizations")

# ============================================================
# 6. Add schema to blog pages missing it
# ============================================================
blog_dir = os.path.join(ROOT, "blog")
for fname in os.listdir(blog_dir):
    if not fname.endswith(".html"):
        continue
    path = os.path.join(blog_dir, fname)
    content = read_file(path)
    orig = content
    if 'schema.org' not in content:
        slug = fname.replace(".html", "")
        schema = SCHEMA_LOCALBUSINESS.format(url=f"{DOMAIN}/blog/{slug}")
        content = content.replace('</head>', schema + '\n</head>')
        write_file(path, content)
        print(f"Added schema to blog/{fname}")

print("All fixes applied.")
