#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

DOMAINS_URL = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/whitelist.txt"
CIDR_URL = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/cidrwhitelist.txt"

OUT_DIR = "dist"
SURGE_DIR = os.path.join(OUT_DIR, "surge")
LOON_DIR = os.path.join(OUT_DIR, "loon")

COMMENT_PREFIXES = ("#", "//", ";")

DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+$")

def fetch_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ru-smart-rules-bot/1.0 (+github actions)"
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

def clean_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith(COMMENT_PREFIXES):
            continue
        # 去掉行内注释（保守：只处理 # 之后）
        if "#" in s:
            s = s.split("#", 1)[0].strip()
        if not s:
            continue
        lines.append(s)
    return lines

def normalize_domain(s: str) -> str | None:
    s = s.strip()
    if not s:
        return None

    # 如果上游有写协议/路径，裁掉
    s = re.sub(r"^https?://", "", s, flags=re.I)
    s = s.split("/", 1)[0].strip()

    # 去掉端口
    if ":" in s and not re.match(r"^\[.*\]$", s):
        host, maybe_port = s.rsplit(":", 1)
        if maybe_port.isdigit():
            s = host

    # 去掉前导点、通配
    s = s.lstrip(".")
    if s.startswith("*."):
        s = s[2:]

    s = s.lower().strip()
    if not s:
        return None

    # 排除明显不是域名的
    if "/" in s or " " in s:
        return None
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", s):
        return None

    # 基本域名校验（允许 punycode）
    if DOMAIN_RE.match(s) or s.startswith("xn--"):
        return s

    return None

def normalize_cidr(s: str) -> str | None:
    s = s.strip()
    if not s:
        return None
    # 去掉尾部注释/多余字段
    s = s.split(",", 1)[0].strip()
    s = s.split(" ", 1)[0].strip()
    if not s:
        return None
    # 简单校验 CIDR
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$", s):
        return s
    return None

def write_file(path: str, lines: list[str]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip() + "\n")

def header(title: str, source: str) -> list[str]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    return [
        f"# {title}",
        f"# Generated at: {now}",
        f"# Source: {source}",
        "#",
    ]

def main() -> int:
    domains_txt = fetch_text(DOMAINS_URL)
    cidr_txt = fetch_text(CIDR_URL)

    domains_raw = clean_lines(domains_txt)
    cidr_raw = clean_lines(cidr_txt)

    domains: list[str] = []
    for s in domains_raw:
        d = normalize_domain(s)
        if d:
            domains.append(d)

    cidrs: list[str] = []
    for s in cidr_raw:
        c = normalize_cidr(s)
        if c:
            cidrs.append(c)

    # 去重排序
    domains = sorted(set(domains))
    cidrs = sorted(set(cidrs))

    # 输出：Surge
    surge_domains = header("RU Direct Domains (Surge)", DOMAINS_URL) + [f"DOMAIN-SUFFIX,{d}" for d in domains]
    surge_cidrs = header("RU Direct CIDRs (Surge)", CIDR_URL) + [f"IP-CIDR,{c},no-resolve" for c in cidrs]

    # 输出：Loon（Loon 也支持这套语法）
    loon_domains = header("RU Direct Domains (Loon)", DOMAINS_URL) + [f"DOMAIN-SUFFIX,{d}" for d in domains]
    loon_cidrs = header("RU Direct CIDRs (Loon)", CIDR_URL) + [f"IP-CIDR,{c},no-resolve" for c in cidrs]

    write_file(os.path.join(SURGE_DIR, "ru_direct_domains.list"), surge_domains)
    write_file(os.path.join(SURGE_DIR, "ru_direct_cidrs.list"), surge_cidrs)
    write_file(os.path.join(LOON_DIR, "ru_direct_domains.list"), loon_domains)
    write_file(os.path.join(LOON_DIR, "ru_direct_cidrs.list"), loon_cidrs)

    print(f"Domains: {len(domains)}")
    print(f"CIDRs:   {len(cidrs)}")
    print("Done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
