#!/usr/bin/env python3
"""
DNS Block List Merger
Downloads block lists from sources defined in lists.yaml and merges them into a single file.
"""

import yaml
import requests
import re
import sys
from pathlib import Path
from typing import Set, List
from datetime import datetime

def load_sources(yaml_file: str = "lists.yaml") -> List[str]:
    """Load block list sources from YAML file."""
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('blocklists', [])
    except FileNotFoundError:
        print(f"Error: {yaml_file} not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

def download_blocklist(url: str) -> Set[str]:
    """Download and parse a block list from URL."""
    domains = set()

    try:
        print(f"Downloading: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        for line in response.text.splitlines():
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Extract domain from hosts file format (0.0.0.0 domain.com or 127.0.0.1 domain.com)
            if line.startswith('0.0.0.0 ') or line.startswith('127.0.0.1 '):
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[1].lower().strip()
                    # Validate domain format
                    if is_valid_domain(domain):
                        domains.add(domain)

            # Handle plain domain lists (one domain per line)
            elif is_valid_domain(line.lower()):
                domains.add(line.lower())

        print(f"  → Found {len(domains)} domains")
        return domains

    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return set()

def is_valid_domain(domain: str) -> bool:
    """Validate domain format."""
    # Skip localhost and invalid entries
    if domain in ['localhost', 'local', 'broadcasthost', '0.0.0.0', '127.0.0.1']:
        return False

    # Basic domain validation regex
    domain_pattern = re.compile(
        r'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$'
    )

    return bool(domain_pattern.match(domain)) and '.' in domain

def merge_blocklists(sources: List[str]) -> Set[str]:
    """Download and merge all block lists."""
    all_domains = set()

    for url in sources:
        domains = download_blocklist(url)
        all_domains.update(domains)

    return all_domains

def write_merged_list(domains: Set[str], output_file: str = "merged-blocklist.txt"):
    """Write merged domains to output file."""
    sorted_domains = sorted(domains)

    with open(output_file, 'w') as f:
        # Write header
        f.write(f"# DNS Block List - Merged from multiple sources\n")
        f.write(f"# Generated on: {datetime.now().isoformat()}\n")
        f.write(f"# Total domains: {len(sorted_domains)}\n")
        f.write(f"#\n")
        f.write(f"# Sources merged:\n")

        sources = load_sources()
        for source in sources:
            f.write(f"# - {source}\n")

        f.write(f"#\n\n")

        # Write domains in hosts file format
        for domain in sorted_domains:
            f.write(f"0.0.0.0 {domain}\n")

    print(f"Merged block list written to {output_file}")
    print(f"Total unique domains: {len(sorted_domains)}")

def main():
    """Main function."""
    print("DNS Block List Merger")
    print("=" * 50)

    # Load sources
    sources = load_sources()
    print(f"Found {len(sources)} sources in lists.yaml")

    if not sources:
        print("No sources found in lists.yaml")
        sys.exit(1)

    # Download and merge
    print("\nDownloading and merging block lists...")
    merged_domains = merge_blocklists(sources)

    if not merged_domains:
        print("No domains found in any source")
        sys.exit(1)

    # Write output
    print(f"\nMerging complete!")
    write_merged_list(merged_domains)

    # Also create a plain domain list (without 0.0.0.0 prefix)
    with open("domains-only.txt", 'w') as f:
        f.write(f"# DNS Block List - Domain names only\n")
        f.write(f"# Generated on: {datetime.now().isoformat()}\n")
        f.write(f"# Total domains: {len(merged_domains)}\n\n")
        for domain in sorted(merged_domains):
            f.write(f"{domain}\n")

    print("Domain-only list written to domains-only.txt")

if __name__ == "__main__":
    main()