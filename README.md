# DNS Block Lists

An automated DNS block list aggregator that downloads and merges multiple block lists into a single, deduplicated list.

## 🚀 Features

- **Automated updates** every 2 days via GitHub Actions
- **Instant updates** when `lists.yaml` is modified
- **Deduplication** - removes duplicate domains across all sources
- **Multiple output formats** - hosts file format and domain-only list
- **Validation** - filters out invalid domains and localhost entries
- **Release automation** - creates tagged releases with statistics

## 📁 Files

### Input
- `lists.yaml` - Configuration file containing source URLs

### Output
- `merged-blocklist.txt` - Complete block list in hosts file format (`0.0.0.0 domain.com`)
- `domains-only.txt` - Domain names only (one per line)

## ⚙️ Configuration

Edit `lists.yaml` to add or remove block list sources:

```yaml
blocklists:
  - https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts
  - https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling/hosts
  - https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts
```

## 🔄 How it works

1. **Scheduled runs**: GitHub Actions runs every 2 days at 2 AM UTC
2. **Manual trigger**: Push changes to `lists.yaml` or manually trigger the workflow
3. **Download**: Fetches all block lists from configured sources
4. **Parse**: Extracts domains from various formats (hosts files, plain domain lists)
5. **Validate**: Filters out invalid domains and localhost entries
6. **Merge**: Combines all sources and removes duplicates
7. **Commit**: Automatically commits updated lists back to the repository
8. **Release**: Creates a tagged release with statistics and download links

## 🛠️ Local Usage

You can run the merger script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the merger
python merge_blocklists.py
```

## 📊 Statistics

The latest merged block list contains domains from multiple reputable sources, providing comprehensive protection against:

- 🚫 Malware and phishing domains
- 📰 Fake news sites
- 🎰 Gambling websites
- 🔞 Adult content
- 📱 Adware and tracking domains

## 🔗 Usage in DNS Servers

### Pi-hole
1. Go to Settings → Blocklists
2. Add the raw URL of `merged-blocklist.txt`
3. Update gravity

### AdGuard Home
1. Go to Filters → DNS blocklists
2. Add the raw URL of `merged-blocklist.txt`
3. Save and update filters

### Unbound
```bash
# Download the domains-only list
curl -o /etc/unbound/blocklist.txt https://raw.githubusercontent.com/yourusername/dns-block-lists/main/domains-only.txt

# Add to unbound.conf:
# include: "/etc/unbound/local-blocking-data.conf"
```

## 📜 License

This project is open source. The individual block lists maintain their respective licenses.

## 🤝 Contributing

1. Fork the repository
2. Add your block list sources to `lists.yaml`
3. Submit a pull request

---

*Last updated automatically via GitHub Actions*