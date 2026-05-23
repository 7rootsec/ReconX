# 🔎 ReconX — Automated Bug Bounty Recon Framework

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Recon-Bug%20Bounty-orange?style=for-the-badge">
  <img src="https://img.shields.io/github/license/7rootsec/ReconX?style=for-the-badge">
</p>

A powerful, all-in-one **automated reconnaissance tool** designed specifically for **bug bounty hunters**, **pentesters**, and **security researchers**.

ReconX automatically discovers subdomains, extracts JS files, scans for endpoints, detects leaked secrets, and performs directory fuzzing — all in one run.



```
[+] Starting full recon for: target.com
[+] Running Subfinder...
[+] Checking alive hosts with httpx...
[+] Extracting JS links...
[+] Scanning JS files...
[+] Running Feroxbuster...
```


# 🌟 Key Features

### 🔍 Subdomain Enumeration

Uses *Subfinder* to gather subdomains.

### 🌐 Alive Host Filtering

Filters reachable domains using *httpx*.

### 📜 JavaScript Discovery

Collects JS files from:
✔ HTML parsing
✔ Katana
✔ WaybackURLs

### ⬇️ JS Downloader

Automatically downloads and stores JavaScript files locally.

### 🕵️ Endpoint Extraction

Extracts:

* API routes
* Full URLs
* Hidden endpoints
* Internal paths

### 🔐 Secret Detection

Finds leaked secrets such as:

* AWS Access Keys
* Firebase API Keys
* Google OAuth tokens
* JWT tokens
* Generic API keys
* Slack tokens
* Private Keys

### 📁 Directory Fuzzing

Runs *Feroxbuster* on the target domain with your custom wordlist.


# 🧩 Architecture Overview

```
Subfinder
    ↓
httpx (Alive Hosts)
    ↓
HTML Parser + Katana + WaybackURLs
    ↓
JS Downloader
    ↓
Endpoint Extractor
    ↓
Secret Detection Engine
    ↓
Feroxbuster (Directory Scan)
```


# 📦 Requirements

### 🐍 Python Modules

```
pip install requests
```

### ⚙️ External Binaries (must be installed)

| Tool            | Usage                |
| --------------- | -------------------- |
| **Subfinder**   | Subdomain discovery  |
| **httpx**       | Alive host checking  |
| **Katana**      | Web crawler          |
| **WaybackURLs** | Crawl archived URLs  |
| **Feroxbuster** | Directory bruteforce |


# 🚀 Installation

```bash
git clone https://github.com/7rootsec/BugBountyRecon-Script
cd BugBountyRecon-Script
python3 recon.py
```


# 🕹 Usage

Run the script:

```bash
python3 recon.py
```

It will ask:

```
Enter target domain (example: target.com):
Enter path to wordlist:
```

Example:

```bash
Enter target domain: example.com
Enter path to wordlist: /usr/share/wordlists/dirb/common.txt
```


# 📁 Output Files

| File                  | Description             |
| --------------------- | ----------------------- |
| **subs.txt**          | Subdomains found        |
| **alive.txt**         | Alive hosts             |
| **js.txt**            | JavaScript URLs         |
| **js_files/**         | Downloaded JS files     |
| **endpoints.txt**     | JS endpoints            |
| **secrets.txt**       | Leaked secrets/API keys |
| **ferox_results.txt** | Directory scan results  |


# 🔥 Ideal For

✔ Bug Bounty Hunters
✔ Web App Pentesters
✔ Recon Automation
✔ CTF Challenges
✔ OSINT + Web Enumeration


# 🛡 Ethical & Legal Disclaimer

This tool is intended solely for **authorized security testing**.
Do **NOT** scan systems without explicit permission.
The author assumes **no responsibility** for misuse.


# ⭐ Support & Contributions

If you like this project:

* ⭐ Star the repository
* 🐛 Report issues
* 🚀 Submit pull requests



## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author


🔗 [GitHub](https://github.com/7rootsec)


##  📞 Contact & Support
If you find any bugs, have questions, or want to suggest improvements, feel free to reach out to me:


Discord: reerdi

