#!/usr/bin/env python3
"""
gsc_inspect_url.py — Inspect a specific URL's index status in Google Search Console.

Shows coverage state, last crawl time, robots.txt status, and any issues.

Usage:
    python3 scripts/gsc_inspect_url.py --site https://example.com/ --url https://example.com/blog/my-post/
    python3 scripts/gsc_inspect_url.py --site https://example.com/ --url https://example.com/page/ --json

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


VERDICT_LABELS = {
    "PASS": "✅ Indexed",
    "PARTIAL": "⚠️ Indexed with issues",
    "FAIL": "❌ Not indexed",
    "NEUTRAL": "ℹ️ Informational",
    "VERDICT_UNSPECIFIED": "❓ Unknown",
}

ROBOTS_LABELS = {
    "ALLOWED": "✅ Allowed",
    "DISALLOWED": "❌ Blocked",
    "ROBOTS_UNSPECIFIED": "❓ Unknown",
}

INDEXING_LABELS = {
    "INDEXING_ALLOWED": "✅ Indexing allowed",
    "BLOCKED_BY_META_TAG": "🚫 Blocked by noindex meta tag",
    "BLOCKED_BY_HTTP_HEADER": "🚫 Blocked by X-Robots-Tag header",
    "BLOCKED_BY_ROBOTS_TXT": "🚫 Blocked by robots.txt",
    "INDEXING_STATE_UNSPECIFIED": "❓ Unknown",
}


def main():
    parser = argparse.ArgumentParser(description="Inspect a URL's index status in Google Search Console")
    parser.add_argument("--site", required=True, help="Site URL (must match GSC property exactly)")
    parser.add_argument("--url", required=True, help="Page URL to inspect")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)

    print(f"Inspecting: {args.url}\n")

    request_body = {
        "inspectionUrl": args.url,
        "siteUrl": args.site,
    }

    try:
        response = service.urlInspection().index().inspect(body=request_body).execute()
    except Exception as e:
        print(f"❌ API error: {e}")
        sys.exit(1)

    result = response.get("inspectionResult", {})

    if args.json:
        print(json.dumps(result, indent=2))
        return

    # Index status
    index_status = result.get("indexStatusResult", {})
    verdict = index_status.get("verdict", "VERDICT_UNSPECIFIED")
    coverage_state = index_status.get("coverageState", "Unknown")
    last_crawl = index_status.get("lastCrawlTime", "Never")
    crawled_as = index_status.get("crawledAs", "Unknown")
    robots_txt_state = index_status.get("robotsTxtState", "ROBOTS_UNSPECIFIED")
    indexing_state = index_status.get("indexingState", "INDEXING_STATE_UNSPECIFIED")
    page_fetch_state = index_status.get("pageFetchState", "Unknown")
    google_canonical = index_status.get("googleCanonical", "Not set")
    user_canonical = index_status.get("userDeclaredCanonical", "Not set")
    referring_urls = index_status.get("referringUrls", [])
    sitemap_urls = index_status.get("sitemap", [])

    print(f"{'='*60}")
    print(f"URL Inspection Report")
    print(f"{'='*60}")
    print(f"Verdict:       {VERDICT_LABELS.get(verdict, verdict)}")
    print(f"Coverage:      {coverage_state}")
    print(f"Last Crawl:    {last_crawl[:19] if last_crawl != 'Never' else 'Never'}")
    print(f"Crawled As:    {crawled_as}")
    print(f"Robots.txt:    {ROBOTS_LABELS.get(robots_txt_state, robots_txt_state)}")
    print(f"Indexing:      {INDEXING_LABELS.get(indexing_state, indexing_state)}")
    print(f"Page Fetch:    {page_fetch_state}")
    print(f"Google Canon:  {google_canonical}")
    print(f"User Canon:    {user_canonical}")

    if sitemap_urls:
        print(f"In Sitemaps:   {', '.join(sitemap_urls)}")
    else:
        print(f"In Sitemaps:   None")

    if referring_urls:
        print(f"Referring URLs: {', '.join(referring_urls[:3])}")

    # Diagnosis hints
    print(f"\n{'='*60}")
    print("Diagnosis:")
    if verdict == "PASS":
        print("  ✅ Page is indexed by Google.")
    elif verdict == "FAIL":
        if "noindex" in indexing_state.lower() or "BLOCKED_BY_META_TAG" in indexing_state:
            print("  🔧 Fix: Remove the <meta name='robots' content='noindex'> tag.")
        elif "BLOCKED_BY_ROBOTS_TXT" in indexing_state or robots_txt_state == "DISALLOWED":
            print("  🔧 Fix: Update robots.txt to allow Googlebot on this URL.")
        elif coverage_state == "Not found (404)":
            print("  🔧 Fix: Page returns 404. Restore the page or set up a redirect.")
        elif coverage_state == "Server error (5xx)":
            print("  🔧 Fix: Server error. Check server logs and stability.")
        elif "Crawled - currently not indexed" in coverage_state:
            print("  🔧 Improve content quality, word count, and internal linking to this page.")
        elif last_crawl == "Never":
            print("  🔧 Page has never been crawled. Add internal links and submit sitemap.")
        else:
            print(f"  ⚠️  Coverage state: {coverage_state}. Check GSC for specific recommendations.")
    elif verdict == "PARTIAL":
        print(f"  ⚠️  Page is indexed but has issues. Coverage: {coverage_state}")
        if google_canonical != args.url:
            print(f"  🔧 Google selected a different canonical: {google_canonical}")
            print(f"     Add <link rel='canonical' href='{args.url}'> if this is the preferred URL.")

    print(f"\nTo request (re)indexing, use GSC > URL Inspection > Request Indexing in the browser.")


if __name__ == "__main__":
    main()
