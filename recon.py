import os
import re
import subprocess
import requests
from urllib.parse import urljoin

# -------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------
def run_cmd(cmd):
    print(f"\n[+] Running: {cmd}\n")
    return subprocess.getoutput(cmd)

# -------------------------------------------------------------
# 1) INPUT
# -------------------------------------------------------------
domain = input("Enter target domain (example: target.com): ").strip()
wordlist = input("Enter path to wordlist: ").strip()

if not domain:
    print("No domain entered. Exiting...")
    exit()

print(f"[+] Starting full recon for: {domain}")

# -------------------------------------------------------------
# 2) SUBFINDER
# -------------------------------------------------------------
print("[+] Running Subfinder...")
run_cmd(f"subfinder -d {domain} -o subs.txt")

# -------------------------------------------------------------
# 3) HTTPX - ALIVE HOSTS
# -------------------------------------------------------------
print("[+] Checking alive hosts with httpx...")
run_cmd("httpx -l subs.txt -o alive.txt")

# Read alive hosts
alive_hosts = open("alive.txt").read().splitlines()

# -------------------------------------------------------------
# 4) JS EXTRACTION FROM HTML
# -------------------------------------------------------------
def extract_js_from_html(url):
    js_files = set()

    try:
        r = requests.get(url, timeout=6)
        html = r.text
    except:
        return js_files

    # <script src="">
    scripts = re.findall(r'<script[^>]+src=["\'](.*?)["\']', html)
    for s in scripts:
        js_files.add(urljoin(url, s))

    # "file.js"
    direct_js = re.findall(r'"(.*?\.js)"', html)
    for s in direct_js:
        js_files.add(urljoin(url, s))

    # loose URLs
    loose = re.findall(r'(https?://[^\'"\s]+\.js)', html)
    for s in loose:
        js_files.add(s)

    return list(js_files)

# -------------------------------------------------------------
# 5) JS FROM KATANA + WAYBACKURLS
# -------------------------------------------------------------
print("[+] Collecting JS using katana + waybackurls...")

katana = run_cmd(f"katana -u https://{domain} -silent")
wayback = run_cmd(f"echo {domain} | waybackurls")

combined = katana.splitlines() + wayback.splitlines()
kat_js = [u for u in combined if ".js" in u]

# -------------------------------------------------------------
# 6) MERGE ALL JS SOURCES
# -------------------------------------------------------------
print("[+] Extracting JS links from alive hosts...")

js_links = set()

for url in alive_hosts:
    found = extract_js_from_html(url)
    if found:
        print(f"[+] {url} → {len(found)} JS files")
        js_links.update(found)
    else:
        print(f"[-] {url} → no JS found")

js_links.update(kat_js)

open("js.txt", "w").write("\n".join(js_links))
print(f"[+] Total JS collected: {len(js_links)}")

# -------------------------------------------------------------
# 7) DOWNLOAD JS FILES
# -------------------------------------------------------------
print("[+] Downloading JS files...")
os.makedirs("js_files", exist_ok=True)

for url in js_links:
    try:
        fname = url.split("/")[-1].split("?")[0]
        path = f"js_files/{fname}"

        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)
            print(f"[+] Saved {fname}")
    except:
        pass

# -------------------------------------------------------------
# 8) ENDPOINT EXTRACTION
# -------------------------------------------------------------
def extract_endpoints(js_code, base_url=None):
    endpoints = set()

    # full URLs
    full = re.findall(r'https?://[^\s\'"]+', js_code)
    endpoints.update(full)

    # simple paths "/api/something"
    paths = re.findall(r'["\'](/[^"\'<>\\s]+)["\']', js_code)
    for p in paths:
        endpoints.add(urljoin(base_url, p) if base_url else p)

    # API routes
    api = re.findall(r'["\'](api/[^"\'<>\\s]+)["\']', js_code)
    for a in api:
        endpoints.add(urljoin(base_url, a) if base_url else a)

    return list(endpoints)

# -------------------------------------------------------------
# 9) SECRET/TOKEN EXTRACTION
# -------------------------------------------------------------
def extract_secrets(js_code):
    leaks = {}

    patterns = {
        "AWS Access Key": r"AKIA[0-9A-Z]{16}",
        "Firebase API Key": r"AIza[0-9A-Za-z\-\_]{35}",
        "Google OAuth": r"ya29\.[0-9A-Za-z\-\_]+",
        "Bearer Token": r"Bearer\s+[A-Za-z0-9\.\-\_]+",
        "JWT": r"eyJ[A-Za-z0-9_\-]+\.{1}[A-Za-z0-9_\-]+\.{1}[A-Za-z0-9_\-]+",
        "Generic API Key": r"(api[-_ ]?key|secret|token)['\" ]*[:=]['\" ]*([A-Za-z0-9_\-]{10,})",
        "Slack Token": r"xox[baprs]-[0-9A-Za-z\-\_]+",
        "Private Key": r"-----BEGIN PRIVATE KEY-----[\s\S]+?-----END PRIVATE KEY-----"
    }

    for name, regex in patterns.items():
        found = re.findall(regex, js_code)
        if found:
            leaks[name] = found

    return leaks

# -------------------------------------------------------------
# 10) SCAN JS FOR ENDPOINTS + SECRETS
# -------------------------------------------------------------
print("[+] Scanning JS files for endpoints and secrets...")

for js_url in js_links:
    try:
        print(f"[+] Scanning: {js_url}")
        js_code = requests.get(js_url, timeout=6).text

        # extract endpoints
        eps = extract_endpoints(js_code, js_url)
        if eps:
            with open("endpoints.txt", "a") as f:
                for ep in eps:
                    f.write(js_url + " -> " + ep + "\n")

        # extract secrets
        secrets = extract_secrets(js_code)
        if secrets:
            with open("secrets.txt", "a") as f:
                for t, vals in secrets.items():
                    f.write(js_url + " -> " + t + ": " + str(vals) + "\n")

    except Exception as e:
        print("Error:", e)

# -------------------------------------------------------------
# 11) FEROXBUSTER
# -------------------------------------------------------------
print("[+] Running Feroxbuster...")
run_cmd(f"feroxbuster -u https://{domain} -w {wordlist} -k -o ferox_results.txt")

# -------------------------------------------------------------
# 12) DONE
# -------------------------------------------------------------
print("\n==============================")
print("      FULL RECON DONE")
print("==============================")
print("[✔] subs.txt")
print("[✔] alive.txt")
print("[✔] js.txt")
print("[✔] js_files/")
print("[✔] endpoints.txt")
print("[✔] secrets.txt")
print("[✔] ferox_results.txt")

