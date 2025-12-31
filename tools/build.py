import re
import urllib.request
from pathlib import Path

DOMAINS_URL = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/whitelist.txt"
CIDR_URL    = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/cidrwhitelist.txt"

OUT_DIR = Path("dist")
OUT_DOMAINS = OUT_DIR / "ru-direct-domains.list"
OUT_CIDR    = OUT_DIR / "ru-direct-cidr.list"

def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode("utf-8", errors="ignore")

def clean_lines(text: str):
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        yield line

def normalize_domain(d: str) -> str | None:
    d = d.strip().lower()
    d = re.sub(r"^https?://", "", d)
    d = d.split("/")[0]
    d = d.split(":")[0]
    d = d.lstrip(".")
    # 非法的直接丢掉
    if not d or " " in d or d.count(".") == 0:
        return None
    return d

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    domains_src = fetch(DOMAINS_URL)
    cidr_src = fetch(CIDR_URL)

    domains = []
    for raw in clean_lines(domains_src):
        d = normalize_domain(raw)
        if d:
            # 一行一个域名 -> 用 DOMAIN-SUFFIX 覆盖子域
            domains.append(f"DOMAIN-SUFFIX,{d}")

    cidrs = []
    for raw in clean_lines(cidr_src):
        raw = raw.split("#")[0].strip()
        if raw:
            cidrs.append(f"IP-CIDR,{raw}")

    OUT_DOMAINS.write_text("\n".join(sorted(set(domains))) + "\n", encoding="utf-8")
    OUT_CIDR.write_text("\n".join(sorted(set(cidrs))) + "\n", encoding="utf-8")

    print(f"OK: {OUT_DOMAINS} ({len(set(domains))})")
    print(f"OK: {OUT_CIDR} ({len(set(cidrs))})")

if __name__ == "__main__":
    main()
