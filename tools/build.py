#!/usr/bin/env python3
import re
import pathlib
import requests

SRC_DOMAINS = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/whitelist.txt"
SRC_CIDRS   = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/cidrwhitelist.txt"

def fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def iter_clean_lines(text: str):
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(("#", "//", ";")):
            continue
        # 去掉行尾注释
        line = re.split(r"\s+#|\s+//", line, 1)[0].strip()
        if line:
            yield line

def main():
    dist = pathlib.Path("dist")
    surge_dir = dist / "surge"
    loon_dir  = dist / "loon"
    surge_dir.mkdir(parents=True, exist_ok=True)
    loon_dir.mkdir(parents=True, exist_ok=True)

    domains = list(iter_clean_lines(fetch(SRC_DOMAINS)))
    cidrs   = list(iter_clean_lines(fetch(SRC_CIDRS)))

    domain_rules = [f"DOMAIN-SUFFIX,{d.lstrip('.')}" for d in domains]

    cidr_rules = []
    for c in cidrs:
        if ":" in c:
            cidr_rules.append(f"IP-CIDR6,{c},no-resolve")
        else:
            cidr_rules.append(f"IP-CIDR,{c},no-resolve")

    # Surge / Loon 的远程 RULE-SET 文件内容格式基本一致：一行一条规则即可
    (surge_dir / "RU_Domains_Direct.list").write_text("\n".join(domain_rules) + "\n", encoding="utf-8")
    (surge_dir / "RU_CIDR_Direct.list").write_text("\n".join(cidr_rules) + "\n", encoding="utf-8")

    (loon_dir / "RU_Domains_Direct.list").write_text("\n".join(domain_rules) + "\n", encoding="utf-8")
    (loon_dir / "RU_CIDR_Direct.list").write_text("\n".join(cidr_rules) + "\n", encoding="utf-8")

    print("Generated:")
    print(" - dist/surge/RU_Domains_Direct.list")
    print(" - dist/surge/RU_CIDR_Direct.list")
    print(" - dist/loon/RU_Domains_Direct.list")
    print(" - dist/loon/RU_CIDR_Direct.list")

if __name__ == "__main__":
    main()
