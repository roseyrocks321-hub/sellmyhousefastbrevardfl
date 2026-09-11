#!/usr/bin/env python3
"""
Add internal links to blog posts and FAQPage schema to city pages.
"""

import os
import re
import json
from pathlib import Path

BASE = Path.home() / "sellmyhousefastbrevardfl"
BLOG_DIR = BASE / "blog"

CITY_PAGES = {
    "melbourne": "/sell-my-house-fast-melbourne",
    "palm bay": "/sell-my-house-fast-palm-bay",
    "titusville": "/sell-my-house-fast-titusville",
    "cocoa": "/sell-my-house-fast-cocoa",
    "cocoa beach": "/sell-my-house-fast-cocoa-beach",
    "rockledge": "/sell-my-house-fast-rockledge",
    "merritt island": "/sell-my-house-fast-merritt-island",
    "satellite beach": "/sell-my-house-fast-satellite-beach",
    "indialantic": "/sell-my-house-fast-indialantic",
    "indian harbour beach": "/sell-my-house-fast-indian-harbour-beach",
    "cape canaveral": "/sell-my-house-fast-cape-canaveral",
    "viera": "/sell-my-house-fast-viera",
    "melbourne beach": "/sell-my-house-fast-melbourne-beach",
}

# Predefined 5 FAQs for each city
CITY_FAQS = {
    "cape-canaveral": [
        ("How fast can I sell my house in Cape Canaveral, FL?",
         "You can sell your Cape Canaveral home for cash in as little as 7 days. We provide a no-obligation cash offer within 24 hours of viewing your property and can close on your schedule. Our cash process bypasses traditional financing delays, inspections, and buyer contingencies."),
        ("Do you buy houses near Port Canaveral and the cruise terminals?",
         "Yes, we purchase homes throughout Cape Canaveral including neighborhoods near Port Canaveral, the cruise terminals, Jetty Park, and the Cape Canaveral Hospital area. Whether your property is close to the beach, along Atlantic Avenue, or in a residential subdivision, we make fair cash offers regardless of location or condition."),
        ("What types of properties do cash buyers purchase in Cape Canaveral?",
         "We buy all types of residential properties in Cape Canaveral including single-family homes, condos, townhomes, duplexes, and vacation rentals. We purchase properties in any condition—whether they need minor cosmetic updates, major renovations, or are completely move-in ready. Even homes with code violations or structural issues are considered."),
        ("How does the Space Coast tourism industry affect Cape Canaveral home sales?",
         "Cape Canaveral's strong tourism and cruise industry creates unique selling opportunities, but also means many homeowners need quick sales when relocating for work. Cash buyers offer certainty and speed that traditional listings cannot match, which is valuable in a market where timing matters for both sellers and buyers."),
        ("Are there any fees or commissions when selling to a cash buyer in Cape Canaveral?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "cocoa-beach": [
        ("How fast can I sell my house in Cocoa Beach, FL?",
         "You can sell your Cocoa Beach property for cash in as little as 7 days. We provide a firm cash offer within 24 hours of viewing your home and can close on your timeline. Our streamlined process eliminates the lengthy escrow periods common in beachside real estate transactions."),
        ("Do you buy homes near the Cocoa Beach Pier and Minuteman Causeway?",
         "Yes, we purchase homes throughout Cocoa Beach including neighborhoods near the Cocoa Beach Pier, Minuteman Causeway, Ron Jon Surf Shop, and along A1A. Whether your property is oceanfront, canal-front, or inland, we make fair cash offers based on current market conditions and your home's specific characteristics."),
        ("What types of properties do you buy in Cocoa Beach?",
         "We buy all residential property types in Cocoa Beach including single-family homes, condos, townhomes, duplexes, and vacation rentals. We purchase properties in any condition—whether they need hurricane repairs, roof replacements, or are fully updated. Even older beach cottages and properties with flood history are considered."),
        ("How does the beach rental market affect selling a home in Cocoa Beach?",
         "Cocoa Beach's popular vacation rental market can make traditional sales complex due to tenant occupancy and seasonal demand fluctuations. Cash buyers can purchase properties with existing tenants or short-term rental agreements in place, giving you flexibility without waiting for leases to expire or dealing with investor financing contingencies."),
        ("Are there any fees or commissions when selling to a cash buyer in Cocoa Beach?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "cocoa": [
        ("How fast can I sell my house in Cocoa, FL?",
         "You can sell your Cocoa home for cash in as little as 7 days. We provide a no-obligation cash offer within 24 hours of viewing your property and can close on your schedule. Our process bypasses the traditional 30-45 day closing timeline by eliminating lender approvals, appraisals, and buyer contingencies."),
        ("Do you buy houses in all Cocoa neighborhoods including Historic Cocoa Village?",
         "Yes, we purchase homes throughout Cocoa including Historic Cocoa Village, Cocoa Hills, College Manor, and neighborhoods near the Indian River. Whether your home is in a historic district, a newer subdivision, or along the river, we make fair cash offers based on local comparable sales and your property's condition."),
        ("What types of properties do cash buyers purchase in Cocoa?",
         "We buy all residential property types in Cocoa including single-family homes, condos, townhomes, duplexes, and inherited properties. We purchase homes in any condition—whether they need minor updates, major renovations, or are move-in ready. Even properties with code violations, liens, or foundation concerns are considered."),
        ("How does Cocoa's location near the Space Coast affect home values?",
         "Cocoa's central Space Coast location with easy access to Orlando, Kennedy Space Center, and Port Canaveral supports steady housing demand. However, this also means homeowners sometimes need fast sales when relocating for aerospace or tourism jobs. Cash buyers provide the speed and certainty that aligns with career-driven moves."),
        ("Are there any fees or commissions when selling to a cash buyer in Cocoa?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "indialantic": [
        ("How fast can I sell my house in Indialantic, FL?",
         "You can sell your Indialantic home for cash in as little as 7 days. We provide a firm cash offer within 24 hours of viewing your property and can close on your schedule. Our streamlined process eliminates the financing delays and inspection contingencies that often complicate beachside real estate transactions."),
        ("Do you buy homes near Indialantic Boardwalk and Fifth Avenue?",
         "Yes, we purchase homes throughout Indialantic including neighborhoods near the Indialantic Boardwalk, Fifth Avenue shops, and along the Indian River Lagoon. Whether your property is oceanfront, riverfront, or in a quiet residential street, we make fair cash offers based on current market conditions and your home's specific condition."),
        ("What types of properties do you buy in Indialantic?",
         "We buy all residential property types in Indialantic including single-family homes, condos, townhomes, and duplexes. We purchase properties in any condition—whether they need hurricane repairs, roof work, or are fully renovated. Even older beach homes and properties with unique characteristics are considered for cash purchase."),
        ("How does the barrier island location affect selling a home in Indialantic?",
         "Indialantic's barrier island location creates both premium values and unique selling challenges including flood insurance requirements and salt air maintenance issues. Cash buyers purchase homes as-is, meaning you do not need to address these coastal concerns before selling. We handle any needed repairs after purchase."),
        ("Are there any fees or commissions when selling to a cash buyer in Indialantic?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "indian-harbour-beach": [
        ("How fast can I sell my house in Indian Harbour Beach, FL?",
         "You can sell your Indian Harbour Beach home for cash in as little as 7 days. We provide a no-obligation cash offer within 24 hours of viewing your property and can close on your timeline. Our cash process eliminates the lender delays and appraisal contingencies common in beachside communities."),
        ("Do you buy homes near Gleason Park and the Indian Harbour Beach Recreation District?",
         "Yes, we purchase homes throughout Indian Harbour Beach including neighborhoods near Gleason Park, the Recreation District, and along A1A. Whether your property is close to the beach, along the Banana River, or in a residential subdivision, we make fair cash offers regardless of location or condition."),
        ("What types of properties do cash buyers purchase in Indian Harbour Beach?",
         "We buy all residential property types in Indian Harbour Beach including single-family homes, condos, townhomes, and duplexes. We purchase properties in any condition—whether they need minor cosmetic work, major renovations, or are completely updated. Even homes with flood history or hurricane damage are considered."),
        ("How does the beachside location affect home sales in Indian Harbour Beach?",
         "Indian Harbour Beach's desirable barrier island location supports strong property values, but also means buyers often have strict inspection and financing requirements related to coastal conditions. Cash buyers offer a faster alternative with no appraisal contingencies or repair demands, allowing you to sell quickly while your home's location premium is still a factor."),
        ("Are there any fees or commissions when selling to a cash buyer in Indian Harbour Beach?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "melbourne-beach": [
        ("How fast can I sell my house in Melbourne Beach, FL?",
         "You can sell your Melbourne Beach property for cash in as little as 7 days. We provide a firm cash offer within 24 hours of viewing your home and can close on your schedule. Our process bypasses the extended timelines common in luxury and waterfront real estate transactions."),
        ("Do you buy homes in all Melbourne Beach neighborhoods including South Beaches?",
         "Yes, we purchase homes throughout Melbourne Beach including the South Beaches area, oceanfront communities, and riverfront neighborhoods along the Indian River Lagoon. Whether your property is a beach cottage, a modern home, or a waterfront estate, we make fair cash offers based on current market conditions."),
        ("What types of properties do you buy in Melbourne Beach?",
         "We buy all residential property types in Melbourne Beach including single-family homes, condos, townhomes, and duplexes. We purchase properties in any condition—whether they need hurricane repairs, roof replacements, or are fully renovated. Even historic beach homes and properties with unique coastal characteristics are considered."),
        ("How does Melbourne Beach's exclusivity affect the selling process?",
         "Melbourne Beach's reputation as an exclusive, low-density community can attract selective buyers with lengthy inspection processes. Cash buyers offer a faster alternative with no financing contingencies or appraisal requirements, allowing you to sell quickly while still receiving fair market value for your property."),
        ("Are there any fees or commissions when selling to a cash buyer in Melbourne Beach?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "melbourne": [
        ("How fast can I sell my house in Melbourne, FL for cash?",
         "You can sell your Melbourne house for cash in as little as 7 days. We provide cash offers within 24 hours of viewing your property and can close on your timeline—whether that's next week or next month. Unlike traditional sales that take 26+ days on average in Melbourne, our cash process eliminates financing delays and buyer contingencies."),
        ("Do you buy houses in all Melbourne neighborhoods?",
         "Yes, we buy houses in all Melbourne neighborhoods including Downtown Melbourne, West Melbourne, Eau Gallie Arts District, Suntree, Viera, Melbourne Beach, and the Airport Area near Orlando Melbourne International Airport. Whether your home is near the Indian River Lagoon, close to the tech corridor along Wickham Road, or in a beachside community, we make fair cash offers regardless of location or condition."),
        ("What types of homes do cash buyers purchase in Melbourne?",
         "We purchase all types of properties in Melbourne including single-family homes, condos, townhouses, duplexes, and inherited properties. We buy houses in any condition—whether they need minor updates, major renovations, or are move-in ready. Even homes with code violations, liens, or foundation issues are considered."),
        ("How does Space Coast's tech industry affect home sales?",
         "Melbourne's booming tech sector with Northrop Grumman, L3Harris, Embraer, and Collins Aerospace has created a competitive housing market. This benefits sellers through steady demand, but tech workers often need to sell quickly when relocating for new positions. Cash buyers provide certainty and speed that aligns with the fast-paced tech industry lifestyle."),
        ("Are there any fees or commissions when selling to a cash buyer in Melbourne?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "merritt-island": [
        ("How fast can I sell my house in Merritt Island, FL?",
         "You can sell your Merritt Island home for cash in as little as 7 days. We provide a no-obligation cash offer within 24 hours of viewing your property and can close on your schedule. Our process eliminates the financing delays common in waterfront and canal-front property transactions."),
        ("Do you buy homes near the Kennedy Space Center and Banana River?",
         "Yes, we purchase homes throughout Merritt Island including neighborhoods near the Kennedy Space Center, along the Banana River, and in the Sykes Creek area. Whether your property is riverfront, canal-front, or in a traditional subdivision, we make fair cash offers based on local comparable sales and your home's condition."),
        ("What types of properties do cash buyers purchase in Merritt Island?",
         "We buy all residential property types in Merritt Island including single-family homes, condos, townhomes, and duplexes. We purchase properties in any condition—whether they need dock repairs, roof work, or are fully updated. Even homes with waterfront wear, flood history, or unique space coast characteristics are considered."),
        ("How does the space industry affect Merritt Island home sales?",
         "Merritt Island's proximity to Kennedy Space Center and Cape Canaveral Space Force Station creates a unique market with aerospace professionals frequently relocating. Cash buyers provide the speed and flexibility needed when job transfers or contract changes require quick home sales without the uncertainty of traditional buyer financing."),
        ("Are there any fees or commissions when selling to a cash buyer in Merritt Island?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "palm-bay": [
        ("How fast can I sell my house in Palm Bay, FL?",
         "You can sell your Palm Bay home for cash in as little as 7 days. We provide a firm cash offer within 24 hours of viewing your property and can close on your timeline. Our streamlined process bypasses the traditional 30+ day closing timeline by eliminating lender approvals, appraisals, and buyer contingencies."),
        ("Do you buy houses in all Palm Bay neighborhoods including Bayside Lakes?",
         "Yes, we purchase homes throughout Palm Bay including Bayside Lakes, Port Malabar, Palm Bay Estates, and neighborhoods along the Indian River. Whether your home is in a gated community, a rural-acreage property, or a traditional subdivision, we make fair cash offers regardless of location or condition."),
        ("What types of properties do cash buyers purchase in Palm Bay?",
         "We buy all residential property types in Palm Bay including single-family homes, condos, townhomes, duplexes, and vacant land with utilities. We purchase properties in any condition—whether they need minor updates, major renovations, or are move-in ready. Even properties with code violations, liens, or well and septic issues are considered."),
        ("How does Palm Bay's growth affect the home selling process?",
         "Palm Bay is one of Florida's fastest-growing cities, which creates strong demand but also means many homeowners need quick sales when relocating for new opportunities. Cash buyers offer certainty in a competitive market, allowing you to sell quickly without waiting for buyer financing or dealing with appraisal gaps common in rapidly appreciating areas."),
        ("Are there any fees or commissions when selling to a cash buyer in Palm Bay?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "rockledge": [
        ("How fast can I sell my house in Rockledge, FL?",
         "You can sell your Rockledge home for cash in as little as 7 days. We provide a no-obligation cash offer within 24 hours of viewing your property and can close on your schedule. Our process eliminates the financing delays and inspection contingencies that can slow down traditional home sales."),
        ("Do you buy homes in all Rockledge neighborhoods including Viera?",
         "Yes, we purchase homes throughout Rockledge including The Villages of Viera East, Rockledge Country Club Estates, and neighborhoods along the Indian River. Whether your home is in a golf course community, a historic area, or a newer subdivision, we make fair cash offers based on local market conditions."),
        ("What types of properties do cash buyers purchase in Rockledge?",
         "We buy all residential property types in Rockledge including single-family homes, condos, townhomes, and duplexes. We purchase properties in any condition—whether they need minor cosmetic work, major renovations, or are completely updated. Even homes with riverfront wear or older infrastructure are considered for cash purchase."),
        ("How does Rockledge's riverfront location affect home values?",
         "Rockledge's position as the oldest city in Brevard County with scenic Indian River frontage supports stable property values. However, riverfront properties can have complex selling requirements. Cash buyers purchase as-is, so you do not need to address seawall issues, dock repairs, or flood zone concerns before selling."),
        ("Are there any fees or commissions when selling to a cash buyer in Rockledge?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "satellite-beach": [
        ("How fast can I sell my house in Satellite Beach, FL?",
         "You can sell your Satellite Beach home for cash in as little as 7 days. We provide a firm cash offer within 24 hours of viewing your property and can close on your timeline. Our cash process eliminates the extended escrow periods and financing contingencies common in beachside real estate."),
        ("Do you buy homes near Hightower Beach Park and Pelican Beach Park?",
         "Yes, we purchase homes throughout Satellite Beach including neighborhoods near Hightower Beach Park, Pelican Beach Park, and along A1A. Whether your property is oceanfront, canal-front, or in a quiet residential neighborhood, we make fair cash offers based on current market conditions and your home's specific condition."),
        ("What types of properties do you buy in Satellite Beach?",
         "We buy all residential property types in Satellite Beach including single-family homes, condos, townhomes, and duplexes. We purchase properties in any condition—whether they need hurricane repairs, roof work, or are fully renovated. Even mid-century beach homes and properties with coastal wear are considered."),
        ("How does Satellite Beach's school reputation affect home sales?",
         "Satellite Beach's highly rated schools create strong buyer demand, but also means traditional buyers often have strict inspection and financing requirements. Cash buyers offer a faster alternative with no appraisal contingencies or repair demands, allowing you to sell quickly while your home's school-district premium is still a factor."),
        ("Are there any fees or commissions when selling to a cash buyer in Satellite Beach?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "titusville": [
        ("How fast can I sell my house in Titusville, FL?",
         "You can sell your Titusville home for cash in as little as 7 days. We provide a no-obligation cash offer within 24 hours of viewing your property and can close on your schedule. Our streamlined process bypasses the traditional 30+ day closing timeline by eliminating lender approvals and buyer contingencies."),
        ("Do you buy houses near Kennedy Space Center and the Indian River?",
         "Yes, we purchase homes throughout Titusville including neighborhoods near Kennedy Space Center, along the Indian River, in La Grange, and in the city center. Whether your home is close to the Space Center, in a historic district, or in a suburban development, we make fair cash offers regardless of location or condition."),
        ("What types of properties do cash buyers purchase in Titusville?",
         "We buy all residential property types in Titusville including single-family homes, condos, townhomes, duplexes, and historic properties. We purchase homes in any condition—whether they need minor updates, major renovations, or are move-in ready. Even properties with space industry-related deferred maintenance are considered."),
        ("How does the space industry affect Titusville home sales?",
         "Titusville's identity as the gateway to Kennedy Space Center means the local housing market is closely tied to aerospace employment cycles. When contractors relocate or programs change, homeowners often need fast sales. Cash buyers provide the speed and certainty that aligns with industry-driven moves without waiting for traditional buyer financing."),
        ("Are there any fees or commissions when selling to a cash buyer in Titusville?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
    "viera": [
        ("How fast can I sell my house in Viera, FL?",
         "You can sell your Viera home for cash in as little as 7 days. We provide a firm cash offer within 24 hours of viewing your property and can close on your timeline. Our process eliminates the financing delays and inspection contingencies that can complicate sales in master-planned communities."),
        ("Do you buy homes in all Viera neighborhoods including Viera East and West?",
         "Yes, we purchase homes throughout Viera including Viera East, Viera West, The Villages of Viera, and neighborhoods near The Avenues shopping district. Whether your home is in a gated community, a golf course neighborhood, or a family-friendly subdivision, we make fair cash offers based on local comparable sales."),
        ("What types of properties do cash buyers purchase in Viera?",
         "We buy all residential property types in Viera including single-family homes, condos, townhomes, and duplexes. We purchase properties in any condition—whether they need minor updates, major renovations, or are move-in ready. Even newer homes with builder defects or properties in active HOA communities are considered."),
        ("How does Viera's master-planned community status affect selling?",
         "Viera's status as a highly desirable master-planned community with top-rated schools attracts quality buyers, but also means strict HOA requirements and longer inspection periods. Cash buyers purchase as-is and can close quickly without requiring HOA approval letters or extensive repair negotiations, saving you time and hassle."),
        ("Are there any fees or commissions when selling to a cash buyer in Viera?",
         "No. When you sell directly to us, there are zero real estate agent commissions, no closing costs, and no hidden fees. The cash offer we present is the amount you receive at closing. We also cover all standard closing costs, so you keep more of your home's equity compared to a traditional sale."),
    ],
}


def build_faq_schema(city_slug):
    faqs = CITY_FAQS.get(city_slug, [])
    if not faqs:
        return None
    main_entity = []
    for q, a in faqs:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }
    return json.dumps(schema, indent=4)


def find_city_mentions(content, filename):
    """Find cities mentioned in content, boosted by filename."""
    lower = content.lower()
    scores = {}
    for city in CITY_PAGES:
        scores[city] = lower.count(city)

    # Boost based on filename
    fname = filename.lower()
    if "melbourne" in fname and "beach" not in fname:
        scores["melbourne"] = scores.get("melbourne", 0) + 100
    if "palm bay" in fname or "palmbay" in fname:
        scores["palm bay"] = scores.get("palm bay", 0) + 100
    if "titusville" in fname:
        scores["titusville"] = scores.get("titusville", 0) + 100
    if "cocoa beach" in fname or "cocoabeach" in fname:
        scores["cocoa beach"] = scores.get("cocoa beach", 0) + 100
    elif "cocoa" in fname:
        scores["cocoa"] = scores.get("cocoa", 0) + 100
    if "rockledge" in fname:
        scores["rockledge"] = scores.get("rockledge", 0) + 100
    if "merritt island" in fname or "merrittisland" in fname:
        scores["merritt island"] = scores.get("merritt island", 0) + 100
    if "satellite beach" in fname or "satellitebeach" in fname:
        scores["satellite beach"] = scores.get("satellite beach", 0) + 100
    if "indialantic" in fname:
        scores["indialantic"] = scores.get("indialantic", 0) + 100
    if "indian harbour beach" in fname or "indianharbour" in fname:
        scores["indian harbour beach"] = scores.get("indian harbour beach", 0) + 100
    if "cape canaveral" in fname or "capecanaveral" in fname:
        scores["cape canaveral"] = scores.get("cape canaveral", 0) + 100
    if "viera" in fname:
        scores["viera"] = scores.get("viera", 0) + 100
    if "melbourne beach" in fname or "melbournebeach" in fname:
        scores["melbourne beach"] = scores.get("melbourne beach", 0) + 100

    # Filter out cities already linked
    filtered = {}
    for city, score in scores.items():
        if score > 0 and f'href="{CITY_PAGES[city]}"' not in content:
            filtered[city] = score

    return sorted(filtered.items(), key=lambda x: x[1], reverse=True)


def add_blog_links(filepath):
    content = filepath.read_text(encoding="utf-8")
    original = content
    filename = filepath.name

    if filename == "index.html":
        return False

    cities = find_city_mentions(content, filename)
    if not cities:
        return False

    # Pick top 1-2 cities
    selected = [c for c, s in cities[:2]]
    if not selected:
        return False

    # Find a good insertion point: after the first paragraph that mentions one of the selected cities
    # and is NOT inside a heading, list, or CTA box.
    inserted = set()
    for city in selected:
        if city in inserted:
            continue
        url = CITY_PAGES[city]
        # Create contextual sentence based on city
        city_title = city.title()
        if city == "cape canaveral":
            city_title = "Cape Canaveral"
        elif city == "cocoa beach":
            city_title = "Cocoa Beach"
        elif city == "melbourne beach":
            city_title = "Melbourne Beach"
        elif city == "satellite beach":
            city_title = "Satellite Beach"
        elif city == "indian harbour beach":
            city_title = "Indian Harbour Beach"
        elif city == "palm bay":
            city_title = "Palm Bay"
        elif city == "merritt island":
            city_title = "Merritt Island"

        link_html = f'<p>If you need to <a href="{url}" style="color:#2c5282;text-decoration:none;font-weight:500;">sell your house fast in {city_title}</a>, we buy homes for cash throughout the area. No repairs, no fees, close in days.</p>'

        # Try to find first paragraph containing the city name (case-insensitive)
        # Use regex to find <p> tags that contain the city
        pattern = re.compile(rf'(<p[^>]*>)(?![^<]*<a[^>]*href="{re.escape(url)}"[^>]*>)([^<]*{re.escape(city_title)}[^<]*)(</p>)', re.IGNORECASE)
        match = pattern.search(content)
        if match:
            insert_pos = match.end()
            if link_html not in content:
                content = content[:insert_pos] + "\n" + link_html + content[insert_pos:]
                inserted.add(city)
                continue

        # Fallback: insert after first </h1> if no matching paragraph
        if not inserted:
            h1_end = content.lower().find('</h1>')
            if h1_end != -1:
                insert_pos = h1_end + 5
                if link_html not in content:
                    content = content[:insert_pos] + "\n" + link_html + content[insert_pos:]
                    inserted.add(city)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def replace_faq_schema(filepath):
    content = filepath.read_text(encoding="utf-8")
    original = content
    filename = filepath.name

    city_slug = filename.replace("sell-my-house-fast-", "").replace(".html", "")
    if city_slug not in CITY_FAQS:
        return False

    faq_json = build_faq_schema(city_slug)
    if not faq_json:
        return False

    # Remove ALL FAQPage schema blocks robustly
    # Match from <!-- FAQ ... --> or <script> up to closing </script> that contains FAQPage
    # We'll iterate to remove all occurrences
    removed = False
    for _ in range(20):  # safety limit
        # Find any script tag containing FAQPage
        match = re.search(r'<script\s+type=["\']application/ld+json["\']\s*>(.*?)FAQPage(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
        if not match:
            break
        start = match.start()
        end = match.end()
        # Also remove preceding comment like <!-- FAQ Schema -->
        before = content[:start]
        comment_match = re.search(r'<!--\s*FAQ[^>]*-->\s*$', before, re.IGNORECASE)
        if comment_match:
            start = comment_match.start()
        content = content[:start] + content[end:]
        removed = True

    # Clean up extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Insert new FAQPage schema before </head>
    new_script = f'''    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {faq_json}
    </script>
'''

    head_close = content.lower().find('</head>')
    if head_close != -1:
        # Insert with a newline before
        content = content[:head_close] + new_script + content[head_close:]
    else:
        body_start = content.lower().find('<body>')
        if body_start != -1:
            content = content[:body_start] + new_script + content[body_start:]

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    modified = []

    for filepath in sorted(BLOG_DIR.glob("*.html")):
        if filepath.name == "index.html":
            continue
        if add_blog_links(filepath):
            modified.append(f"blog/{filepath.name}")
            print(f"Modified blog/{filepath.name}")

    for filepath in sorted(BASE.glob("sell-my-house-fast-*.html")):
        if replace_faq_schema(filepath):
            modified.append(filepath.name)
            print(f"Modified {filepath.name}")

    print(f"\nTotal modified files: {len(modified)}")
    for m in modified:
        print(f"  - {m}")


if __name__ == "__main__":
    main()
