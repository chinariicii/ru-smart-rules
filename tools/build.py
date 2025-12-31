import os
import urllib.request
import ssl

# --- 1. 配置部分 ---
URL_DOMAINS = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/whitelist.txt"
URL_CIDRS   = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/cidrwhitelist.txt"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)
DIST_DIR = os.path.join(REPO_ROOT, "dist")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# --- 2. 功能函数 ---

def fetch_data(url):
    print(f"Fetching {url}...")
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=30) as f:
            return f.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def clean_lines(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(('#', ';', '//')):
            continue
        if '#' in line:
            line = line.split('#')[0].strip()
        if line:
            lines.append(line)
    return sorted(list(set(lines)))

def fix_cidr_format(ip_str):
    """
    修复 CIDR 格式：
    如果 IP 自带掩码 (如 1.2.3.0/24)，保持不变。
    如果 IP 没有掩码 (如 1.2.3.4)，自动补全 /32 (IPv4) 或 /128 (IPv6)。
    """
    if '/' in ip_str:
        return ip_str
    
    # 简单的 IPv6 判断
    if ':' in ip_str:
        return f"{ip_str}/128"
    
    # 默认为 IPv4
    return f"{ip_str}/32"

def save_file(subfolder, filename, lines):
    folder_path = os.path.join(DIST_DIR, subfolder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    content = '\n'.join(lines) + '\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved: {file_path} ({len(lines)} lines)")

# --- 3. 主程序 ---

def main():
    raw_domains = fetch_data(URL_DOMAINS)
    raw_cidrs = fetch_data(URL_CIDRS)

    clean_domains = clean_lines(raw_domains)
    clean_cidrs = clean_lines(raw_cidrs)

    # 生成 Surge 域名规则
    surge_domains = [f"DOMAIN-SUFFIX,{d}" for d in clean_domains]
    
    # 生成 Surge IP 规则 (这里调用了 fix_cidr_format 来补全 /32)
    surge_cidrs = [f"IP-CIDR,{fix_cidr_format(c)},no-resolve" for c in clean_cidrs]

    # 保存 Surge 文件
    save_file("surge", "ru_whitelist_domains.list", surge_domains)
    save_file("surge", "ru_whitelist_cidrs.list", surge_cidrs)

    # 保存 Loon 文件 (Loon 也能识别 /32，所以直接通用即可)
    save_file("loon", "ru_whitelist_domains.list", surge_domains)
    save_file("loon", "ru_whitelist_cidrs.list", surge_cidrs)

if __name__ == "__main__":
    main()
