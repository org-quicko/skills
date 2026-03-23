#!/usr/bin/env python3
"""
gsc_index_coverage.py — Pull index coverage data from Google Search Console.

Lists pages by status: Valid, Valid with Warning, Error, Excluded.

Usage:
    python3 scripts/gsc_index_coverage.py --site https://example.com/
    python3 scripts/gsc_index_coverage.py --site https://example.com/ --status Error
    python3 scripts/gsc_index_coverage.py --site https://example.com/ --json

Requires:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

    Set GSC_CREDENTIALS_FILE env var to path of your OAuth2 credentials JSON.
"""

import argparse
import json
import os
import sys

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Missing dependencies. Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
TOKEN_FILE = os.path.expanduser("~/.gsc_token.json")

VERDICT_EMOJI = {
    "PASS": "✅",
    "PARTIAL": "⚠️",
    "FAIL": "❌",
    "NEUTRAL": "ℹ️",
    "VERDICT_UNSPECIFIED": "❓",
}

COVERAGE_STATE_LABELS = {
    "Submitted and indexed": "✅ Indexed",
    "Indexed, not submitted in sitemap": "✅ Indexed (not in sitemap)",
    "Crawled - currently not indexed": "⚠️ Not indexed",
    "Discovered - currently not indexed": "⚠️ Discovered, not indexed",
    "Page with redirect": "↩️ Redirect",
    "Duplicate without user-selected canonical": "⚠️ Duplicate",
    "Duplicate, submitted URL not selected as canonical": "⚠️ Duplicate (canonical mismatch)",
    "URL is unknown to Google": "❓ Unknown",
    "Excluded by 'noindex' tag": "🚫 noindex",
    "Blocked by robots.txt": "🚫 Blocked (robots.txt)",
    "Not found (404)": "❌ 404 Not Found",
    "Server error (5xx)": "❌ Server Error",
    "Soft 404": "⚠️ Soft 404",
}


def get_credentials():
    creds = None
    creds_file = os.environ.get("GSC_CREDENTIALS_FILE")

    if not creds_file:
        print("Error: Set GSC_CREDENTIALS_FILE environment variable to your OAuth2 credentials JSON path.")
        sys.exit(1)

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds


def fetch_url_inspection(service, site_url, page_url):
    """Inspect a single URL and return coverage details."""
    request_body = {
        "inspectionUrl": page_url,
        "siteUrl": site_url,
    }
    try:
        result = service.urlInspection().index().inspect(body=request_body).execute()
        return result.get("inspectionResult", {})
    except Exception as e:
        return {"error": str(e)}


def fetch_sitemaps(service, site_url):
    """List all sitemaps and get submitted URLs."""
    try:
        response = service.sitemaps().list(siteUrl=site_url).execute()
        return response.get("sitemap", [])
    except Exception as e:
        return []


def main():
    parser = argparse.ArgumentParser(description="Check Google Search Console index coverage")
    parser.add_argument("--site", required=True, help="Site URL (must match GSC property exactly)")
    parser.add_argument("--urls", nargs="+", help="Specific URLs to inspect (space-separated). If not provided, checks sitemaps.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)

    urls_to_check = args.urls or []

    # If no URLs specified, try to get URLs from sitemaps
    if not urls_to_check:
        print(f"No specific URLs provided. Fetching sitemap data for {args.site}...\n")
        sitemaps = fetch_sitemaps(service, args.site)

        if sitemaps:
            print("Sitemaps found:")
            for sm in sitemaps:
                status = "✅" if sm.get("isPending") is False else "⏳"
                errors = sm.get("errors", 0)
                warnings = sm.get("warnings", 0)
                contents = sm.get("contents", [])
                total_submitted = sum(c.get("submitted", 0) for c in contents)
                total_indexed = sum(c.get("indexed", 0) for c in contents)
                print(f"  {status} {sm['path']}")
                print(f"     Submitted: {total_submitted} | Indexed: {total_indexed} | Errors: {errors} | Warnings: {warnings}")
                if errors > 0:
                    print(f"     ⚠️  Sitemap has {errors} errors — check GSC > Indexing > Sitemaps for details")
        else:
            print("No sitemaps found. Consider submitting a sitemap via GSC > Indexing > Sitemaps.")

        print("\nTo inspect specific URLs, run:")
        print(f"  python3 scripts/gsc_index_coverage.py --site {args.site} --urls URL1 URL2 URL3")
        return

    # Inspect each URL
    print(f"Inspecting {len(urls_to_check)} URLs for {args.site}...\n")
    results = []

    for url in urls_to_check:
        inspection = fetch_url_inspection(service, args.site, url)

        if "error" in inspection:
            results.append({"url": url, "status": "Error", "detail": inspection["error"]})
            continue

        index_status = inspection.get("indexStatusResult", {})
        verdict = index_status.get("verdict", "VERDICT_UNSPECIFIED")
        coverage_state = index_status.get("coverageState", "Unknown")
        last_crawl = index_status.get("lastCrawlTime", "Never")
        crawled_as = index_status.get("crawledAs", "Unknown")
        robots_txt_state = index_status.get("robotsTxtState", "Unknown")
        indexing_state = index_status.get("indexingState", "Unknown")

        results.append({
            "url": url,
            "verdict": f"{VERDICT_EMOJI.get(verdict, '❓')} {verdict}",
            "coverage": COVERAGE_STATE_LABELS.get(coverage_state, coverage_state),
            "last_crawl": last_crawl[:10] if last_crawl != "Never" else "Never",
            "crawled_as": crawled_as,
            "robots": robots_txt_state,
        })

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Print results
    for r in results:
        print(f"URL: {r['url']}")
        print(f"  Status:    {r.get('verdict', r.get('status', 'Unknown'))}")
        if "coverage" in r:
            print(f"  Coverage:  {r['coverage']}")
            print(f"  Last crawl: {r['last_crawl']}")
            print(f"  Crawled as: {r['crawled_as']}")
            print(f"  Robots:    {r['robots']}")
        elif "detail" in r:
            print(f"  Detail: {r['detail']}")
        print()

    # Summary
    verdicts = [r.get("verdict", "") for r in results]
    passed = sum(1 for v in verdicts if "PASS" in v)
    failed = sum(1 for v in verdicts if "FAIL" in v)
    partial = sum(1 for v in verdicts if "PARTIAL" in v)

    print(f"Summary: {passed} indexed ✅ | {partial} warnings ⚠️ | {failed} errors ❌")


if __name__ == "__main__":
    main()
