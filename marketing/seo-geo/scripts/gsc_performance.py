#!/usr/bin/env python3
"""
gsc_performance.py — Pull clicks, impressions, CTR, and position data from Google Search Console.

Usage:
    python3 scripts/gsc_performance.py --site https://example.com/ --days 90 --dimension query
    python3 scripts/gsc_performance.py --site https://example.com/ --days 90 --dimension page
    python3 scripts/gsc_performance.py --site https://example.com/ --days 28 --dimension query --limit 50

Requires:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client tabulate

    Set GSC_CREDENTIALS_FILE env var to path of your OAuth2 credentials JSON (from Google Cloud Console).
    On first run, a browser will open for OAuth consent. Token is cached in ~/.gsc_token.json.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

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
        print("Download from: Google Cloud Console > APIs & Services > Credentials > OAuth 2.0 Client ID")
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


def fetch_performance(site_url, start_date, end_date, dimension, limit=100):
    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)

    request_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": [dimension],
        "rowLimit": limit,
        "startRow": 0,
    }

    response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
    return response.get("rows", [])


def format_rows(rows, dimension):
    results = []
    for row in rows:
        results.append({
            dimension: row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": f"{row.get('ctr', 0) * 100:.1f}%",
            "position": f"{row.get('position', 0):.1f}",
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch Google Search Console performance data")
    parser.add_argument("--site", required=True, help="Site URL (must match GSC property exactly, e.g. https://example.com/)")
    parser.add_argument("--days", type=int, default=90, help="Number of days back (default: 90)")
    parser.add_argument("--dimension", choices=["query", "page", "country", "device"], default="query", help="Dimension to group by")
    parser.add_argument("--limit", type=int, default=25, help="Number of rows to return (default: 25, max: 25000)")
    parser.add_argument("--min-impressions", type=int, default=0, help="Filter rows with impressions above this threshold")
    parser.add_argument("--max-position", type=float, default=None, help="Filter rows below this average position")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of table")
    args = parser.parse_args()

    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    print(f"Fetching GSC performance data for {args.site}")
    print(f"Date range: {start_date} to {end_date} | Dimension: {args.dimension}\n")

    rows = fetch_performance(args.site, start_date, end_date, args.dimension, limit=args.limit)
    results = format_rows(rows, args.dimension)

    # Apply filters
    if args.min_impressions:
        results = [r for r in results if r["impressions"] >= args.min_impressions]
    if args.max_position:
        results = [r for r in results if float(r["position"]) <= args.max_position]

    if not results:
        print("No data found for the given parameters.")
        return

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Table output
    try:
        from tabulate import tabulate
        headers = list(results[0].keys())
        rows_out = [[r[h] for h in headers] for r in results]
        print(tabulate(rows_out, headers=headers, tablefmt="rounded_outline"))
    except ImportError:
        # Fallback: plain text
        headers = list(results[0].keys())
        print("\t".join(headers))
        for r in results:
            print("\t".join(str(r[h]) for h in headers))

    print(f"\nTotal rows: {len(results)}")

    # Highlight quick wins
    low_ctr = [r for r in results if float(r["ctr"].rstrip("%")) < 2.0 and r["impressions"] > 500]
    near_page1 = [r for r in results if 5 <= float(r["position"]) <= 20]

    if low_ctr and args.dimension == "query":
        print(f"\n⚠️  Quick win — {len(low_ctr)} queries with >500 impressions but CTR < 2% (improve meta titles/descriptions):")
        for r in low_ctr[:5]:
            print(f"   '{r['query']}' — {r['impressions']} impressions, {r['ctr']} CTR, pos {r['position']}")

    if near_page1 and args.dimension == "query":
        print(f"\n🎯 Optimization targets — {len(near_page1)} queries ranked 5–20 (close to page 1):")
        for r in near_page1[:5]:
            print(f"   '{r['query']}' — pos {r['position']}, {r['impressions']} impressions")


if __name__ == "__main__":
    main()
