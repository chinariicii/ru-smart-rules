import os
import urllib.request
import ssl

# 1. 定义源地址
URL_DOMAINS = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/whitelist.txt"
URL_CIDRS   = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/cidrwhitelist.txt"

# 2. 定义输出文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)
DIST_DIR = os.path.join(REPO_ROOT, "dist")

# 创建忽略 SSL 错误的上下文（防止 GitHub Actions 有时抽风）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

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
        # 跳过空行和注释
        if not line or line.startswith(('#', ';', '//')):
            continue
        # 去除行内注释
        if '#' in line:
            line = line.split('#')[0].strip()
        if line:
            lines.append(line)
    return sorted(list(set(lines))) # 去重 + 排序

def save_file(subfolder, filename, lines):
    folder_path = os.path.join(DIST_DIR, subfolder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"Saved: {file_path} ({len(lines)} lines)")

def main():
    # 获取原始数据
    raw_domains = fetch_data(URL_DOMAINS)
    raw_cidrs = fetch_data(URL_CIDRS)

    # 清洗数据
    clean_domains = clean_lines(raw_domains)
    clean_cidrs = clean_lines(raw_cidrs)

    # --- 生成 Surge 格式 ---
    # 域名加 DOMAIN-SUFFIX
    surge_domains = [f"DOMAIN-SUFFIX,{d}" for d in clean_domains]
    # IP 加 IP-CIDR, ..., no-resolve
    surge_cidrs = [f"IP-CIDR,{c},no-resolve" for c in clean_cidrs]

    save_file("surge", "ru_whitelist_domains.list", surge_domains)
    save_file("surge", "ru_whitelist_cidrs.list", surge_cidrs)

    # --- 生成 Loon 格式 (Loon 其实兼容 Surge 格式，这里做一份一模一样的即可) ---
    save_file("loon", "ru_whitelist_domains.list", surge_domains)
    save_file("loon", "ru_whitelist_cidrs.list", surge_cidrs)

if __name__ == "__main__":
    main()
