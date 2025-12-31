import os
import urllib.request
import ssl

# --- 1. 配置部分 ---
# 源文件地址
URL_DOMAINS = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/whitelist.txt"
URL_CIDRS   = "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/cidrwhitelist.txt"

# 定义输出文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)
DIST_DIR = os.path.join(REPO_ROOT, "dist")

# 创建忽略 SSL 错误的上下文
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# --- 2. 功能函数 ---

def fetch_data(url):
    """从网络获取数据"""
    print(f"Fetching {url}...")
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=30) as f:
            return f.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None  # 返回 None 表示失败，而不是空字符串

def clean_lines(text):
    """清洗数据：去空行、去注释、去重、排序"""
    if text is None: 
        return []
    
    lines = []
    for line in text.splitlines():
        line = line.strip()
        # 跳过空行和整行注释
        if not line or line.startswith(('#', ';', '//')):
            continue
        # 去除行内注释
        if '#' in line:
            line = line.split('#')[0].strip()
        
        if line:
            lines.append(line)
    return sorted(list(set(lines)))

def format_cidr(ip_line):
    """核心修复：处理 IP CIDR 格式，自动补全 /32 或 /128"""
    try:
        # 如果已经包含 / (例如 1.2.3.0/24)，直接返回
        if '/' in ip_line:
            return f"IP-CIDR,{ip_line},no-resolve"
        
        # 判断是 IPv6 (包含冒号) 还是 IPv4
        if ':' in ip_line:
            # IPv6 且没后缀，补全 /128
            return f"IP-CIDR6,{ip_line}/128,no-resolve"
        else:
            # IPv4 且没后缀，补全 /32
            return f"IP-CIDR,{ip_line}/32,no-resolve"
    except Exception:
        return None

def save_file(subfolder, filename, lines):
    """保存文件"""
    if not lines:
        print(f"⚠️ Warning: No content to save for {filename}, skipping to prevent empty file.")
        return

    folder_path = os.path.join(DIST_DIR, subfolder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    content = '\n'.join(lines) + '\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Saved: {file_path} ({len(lines)} lines)")

# --- 3. 主程序 ---

def main():
    # 1. 获取原始数据
    raw_domains = fetch_data(URL_DOMAINS)
    raw_cidrs = fetch_data(URL_CIDRS)

    # 如果两者都获取失败，直接退出，不要覆盖旧文件
    if raw_domains is None and raw_cidrs is None:
        print("❌ Critical: Failed to fetch both sources. Aborting.")
        return

    # 2. 清洗数据
    clean_domain_list = clean_lines(raw_domains)
    clean_cidr_list = clean_lines(raw_cidrs)

    # 3. 转换格式 (Surge / Loon)
    
    # --- 处理域名 ---
    surge_domains = [f"DOMAIN-SUFFIX,{d}" for d in clean_domain_list]
    
    # --- 处理 IP (核心修复点) ---
    surge_cidrs = []
    for c in clean_cidr_list:
        formatted = format_cidr(c)
        if formatted:
            surge_cidrs.append(formatted)

    # 4. 保存文件
    
    # 保存 Surge 格式
    save_file("surge", "ru_whitelist_domains.list", surge_domains)
    save_file("surge", "ru_whitelist_cidrs.list", surge_cidrs)

    # 保存 Loon 格式 (如果需要的话)
    save_file("loon", "ru_whitelist_domains.list", surge_domains)
    save_file("loon", "ru_whitelist_cidrs.list", surge_cidrs)

if __name__ == "__main__":
    main()
