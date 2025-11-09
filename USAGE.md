# Usage Examples

## Adding New Block List Sources

Edit `lists.yaml` to add new sources:

```yaml
blocklists:
  - https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts
  - https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling/hosts
  - https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts
  # Add your new sources here:
  - https://somehost.com/path/to/blocklist.txt
  - https://example.org/malware-domains.hosts
```

## Supported Input Formats

The merger script supports multiple block list formats:

### Hosts File Format
```
# Comments are ignored
0.0.0.0 malicious-site.com
127.0.0.1 bad-domain.org
```

### Plain Domain Lists
```
# One domain per line
malicious-site.com
bad-domain.org
phishing-site.net
```

## DNS Server Integration

### Pi-hole
1. Copy the raw URL: `https://raw.githubusercontent.com/yourusername/dns-block-lists/main/merged-blocklist.txt`
2. Go to Pi-hole Admin → Settings → Blocklists
3. Paste the URL and click "Add"
4. Update gravity

### AdGuard Home
1. Go to Filters → DNS blocklists
2. Click "Add blocklist" → "Add a custom list"
3. Enter name: "Personal DNS Block Lists"
4. Enter URL: `https://raw.githubusercontent.com/yourusername/dns-block-lists/main/merged-blocklist.txt`
5. Save

### pfBlockerNG (pfSense)
1. Go to Firewall → pfBlockerNG → DNSBL
2. Create new group or edit existing
3. Add URL: `https://raw.githubusercontent.com/yourusername/dns-block-lists/main/domains-only.txt`
4. Set format to "Domain List"
5. Save and reload

### Unbound
Add to your unbound configuration:
```
# Download the list
curl -o /var/unbound/blocklist.txt https://raw.githubusercontent.com/yourusername/dns-block-lists/main/domains-only.txt

# Create configuration snippet
echo 'server:' > /var/unbound/blocklist.conf
awk '{print "  local-zone: \""$1"\" refuse"}' /var/unbound/blocklist.txt >> /var/unbound/blocklist.conf

# Include in main config
include: "/var/unbound/blocklist.conf"
```

### BIND9
Create a response policy zone (RPZ):
```
# Convert to RPZ format
awk '{print $1" CNAME ."}' domains-only.txt > blocklist.rpz

# Add to named.conf
zone "blocklist.rpz" {
    type master;
    file "/etc/bind/blocklist.rpz";
};

options {
    response-policy { zone "blocklist.rpz"; };
};
```

## Manual Testing

Test the script locally:
```bash
# Clone the repository
git clone https://github.com/yourusername/dns-block-lists.git
cd dns-block-lists

# Install dependencies
pip install -r requirements.txt

# Run the merger
python merge_blocklists.py

# Check output
head -20 merged-blocklist.txt
wc -l merged-blocklist.txt
```

## Workflow Triggers

The GitHub Actions workflow runs:
- **Automatically**: Every 2 days at 2 AM UTC
- **On changes**: When you push changes to `lists.yaml`
- **Manually**: Click "Run workflow" in the Actions tab

## Monitoring

Check workflow status:
1. Go to the "Actions" tab in your GitHub repository
2. Look for "Update DNS Block Lists" workflows
3. Click on a run to see detailed logs

## Troubleshooting

### Workflow fails with "No changes detected"
This is normal when sources haven't changed since the last run.

### Domain count decreases
This can happen when:
- A source becomes unavailable (temporary or permanent)
- A source removes domains from their list
- A source changes format and domains aren't parsed correctly

### High memory usage
If processing very large lists (millions of domains), consider:
- Using a larger GitHub Actions runner
- Processing sources individually
- Implementing streaming instead of loading everything into memory

## Statistics

View current statistics in the latest release or check the commit messages for domain counts.