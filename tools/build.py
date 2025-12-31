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

# 创建忽略 SSL 错误的上下文（防止 GitHub Actions 有时网络握手失败）
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
        print(f"Error fetching {url}: {e}")
        return ""

def clean_lines(text):
    """清洗数据：去空行、去注释、去重、排序"""
    lines = []
    for line in text.splitlines():
        line = line.strip()
        # 跳过空行和整行注释
        if not line or line.startswith(('#', ';', '//')):
            continue
        # 去除行内注释 (例如: domain.com # comment)
        if '#' in line:
            line = line.split('#')[0].strip()
        
        if line:
            lines.append(line)
    # 去重并排序
    return sorted(list(set(lines)))

def save_file(subfolder, filename, lines):
    """保存文件，确保每行一个规则"""
    folder_path = os.path.join(DIST_DIR, subfolder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    
    # 核心修复：用 '\n'.join() 确保换行，并在文件末尾加一个换行符
    content = '\n'.join(lines) + '\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Saved: {file_path} ({len(lines)} lines)")

# --- 3. 主程序 ---

def main():
    # 1. 获取原始数据
    raw_domains = fetch_data(URL_DOMAINS)
    raw_cidrs = fetch_data(URL_CIDRS)

    # 2. 清洗数据
    clean_domains = clean_lines(raw_domains)
    clean_cidrs = clean_lines(raw_cidrs)

    if not clean_domains:
        print("Warning: No domains found!")
    if not clean_cidrs:
        print("Warning: No CIDRs found!")

    # 3. 转换格式
    # Surge / Loon 域名格式: DOMAIN-SUFFIX,example.com
    surge_domains = [f"DOMAIN-SUFFIX,{d}" for d in clean_domains]
    
    # Surge / Loon IP 格式: IP-CIDR,1.2.3.4/24,no-resolve
    surge_cidrs = [f"IP-CIDR,{c},no-resolve" for c in clean_cidrs]

    # 4. 保存文件 (Surge 和 Loon 格式通用，保存两份只是为了方便订阅分类)
    
    # 保存到 dist/surge/ 目录
    save_file("surge", "ru_whitelist_domains.list", surge_domains)
    save_file("surge", "ru_whitelist_cidrs.list", surge_cidrs)

    # 保存到 dist/loon/ 目录
    save_file("loon", "ru_whitelist_domains.list", surge_domains)
    save_file("loon", "ru_whitelist_cidrs.list", surge_cidrs)

if __name__ == "__main__":
    main()
