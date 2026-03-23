#!/usr/bin/env python3
"""
gsc_sitemaps.py — Manage sitemaps in Google Search Console.

Usage:
    # List all sitemaps
    python3 scripts/gsc_sitemaps.py --site https://example.com/ --action list

    # Submit a sitemap
    python3 scripts/gsc_sitemaps.py --site https://example.com/ --action submit --sitemap https://example.com/sitemap.xml

    # Delete a sitemap
    python3 scripts/gsc_sitemaps.py --site https://example.com/ --action delete --sitemap https://example.com/old-sitemap.xml

Requires:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

    Set GSC_CREDENTIALS_FILE env var to path of your OAuth2 credentials JSON.
    Note: submit/delete require write scope (webmasters scope, not readonly).
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

# Use full webmasters scope for write operations
SCOPES = ["https://www.googleapis.com/auth/webmasters"]
TOKEN_FILE = os.path.expanduser("~/.gsc_token_rw.json")


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


def list_sitemaps(service, site_url):
    response = service.sitemaps().list(siteUrl=site_url).execute()
    sitemaps = response.get("sitemap", [])

    if not sitemaps:
        print(f"No sitemaps found for {site_url}")
        return

    print(f"Sitemaps for {site_url}:\n")
    for sm in sitemaps:
        path = sm.get("path", "")
        last_submitted = sm.get("lastSubmitted", "Unknown")[:10]
        last_downloaded = sm.get("lastDownloaded", "Unknown")[:10]
        is_pending = sm.get("isPending", False)
        errors = sm.get("errors", 0)
        warnings = sm.get("warnings", 0)
        contents = sm.get("contents", [])

        total_submitted = sum(c.get("submitted", 0) for c in contents)
        total_indexed = sum(c.get("indexed", 0) for c in contents)

        status_icon = "⏳" if is_pending else "✅"
        error_str = f" | ❌ {errors} errors" if errors > 0 else ""
        warn_str = f" | ⚠️ {warnings} warnings" if warnings > 0 else ""

        print(f"  {status_icon} {path}")
        print(f"     Submitted: {last_submitted} | Last downloaded: {last_downloaded}")
        print(f"     URLs submitted: {total_submitted} | URLs indexed: {total_indexed}{error_str}{warn_str}")
        print()


def submit_sitemap(service, site_url, sitemap_url):
    try:
        service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
        print(f"✅ Successfully submitted sitemap: {sitemap_url}")
        print("Google will process it within a few days. Check status in GSC > Indexing > Sitemaps.")
    except Exception as e:
        print(f"❌ Failed to submit sitemap: {e}")


def delete_sitemap(service, site_url, sitemap_url):
    try:
        service.sitemaps().delete(siteUrl=site_url, feedpath=sitemap_url).execute()
        print(f"✅ Successfully deleted sitemap: {sitemap_url}")
    except Exception as e:
        print(f"❌ Failed to delete sitemap: {e}")


def main():
    parser = argparse.ArgumentParser(description="Manage Google Search Console sitemaps")
    parser.add_argument("--site", required=True, help="Site URL (must match GSC property exactly)")
    parser.add_argument("--action", choices=["list", "submit", "delete"], required=True)
    parser.add_argument("--sitemap", help="Sitemap URL (required for submit/delete)")
    args = parser.parse_args()

    if args.action in ("submit", "delete") and not args.sitemap:
        print(f"Error: --sitemap is required for action '{args.action}'")
        sys.exit(1)

    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)

    if args.action == "list":
        list_sitemaps(service, args.site)
    elif args.action == "submit":
        submit_sitemap(service, args.site, args.sitemap)
    elif args.action == "delete":
        confirm = input(f"Are you sure you want to delete {args.sitemap}? (yes/no): ")
        if confirm.lower() == "yes":
            delete_sitemap(service, args.site, args.sitemap)
        else:
            print("Aborted.")


if __name__ == "__main__":
    main()
