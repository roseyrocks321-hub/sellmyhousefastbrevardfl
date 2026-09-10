#!/usr/bin/env python3
import os

ROOT = "/Users/rosey./real-estate-websites/brevardfl"

orphaned = [
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

MOBILE_CSS = """
  @media (max-width: 768px) {
    body { margin: 20px auto; padding: 0 15px; }
    h1 { font-size: 24px; }
    h2 { font-size: 18px; }
    .cta-box { padding: 20px; }
    .cta-btn { display: block; width: 100%; text-align: center; }
  }
"""

for fname in orphaned:
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    if "@media" in content:
        continue
    # Insert before </style>
    content = content.replace("</style>", MOBILE_CSS + "\n</style>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Added mobile CSS: {fname}")

print("Done.")
