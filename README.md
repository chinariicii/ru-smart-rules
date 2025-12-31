# ru-smart-rules

🇷🇺 俄罗斯白名单规则转换 (Surge & Loon)

本项目通过 GitHub Actions 自动抓取上游数据，并转换为适用于 Surge、Loon 等工具的规则列表文件。每天定时自动更新。

This project automatically fetches data from the upstream whitelist and converts it into rule sets for Surge, Loon, and other proxy tools. Updates daily.



## 📥 规则订阅 / Subscription

请根据你的需求选择对应的规则文件链接。

| 工具 (Tool) | 链接 (Link) |
| :--- | :--- |
| **Surge 俄罗斯常用域名** | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/refs/heads/main/dist/surge/ru_whitelist_domains.list` |
| **Surge 俄罗斯IP** | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/refs/heads/main/dist/surge/ru_whitelist_cidrs.list` |
| **Loon 俄罗斯常用域名** | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/refs/heads/main/dist/loon/ru_whitelist_domains.list` |
| **Loon 俄罗斯IP** | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/refs/heads/main/dist/loon/ru_whitelist_cidrs.list` |



## ⚙️ 运行机制 / Workflow
GitHub Actions 每天定时触发。

拉取上游最新的 russia-mobile-internet-whitelist 数据。

通过 Python 脚本转换为 Surge/Loon 格式。

自动将生成的规则推送到 dist 目录。


## 🔗 Credits / 致谢

本项目的规则列表数据来源于 [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist)。
感谢原作者维护的俄罗斯移动网络白名单列表。

This project generates Surge & Loon rules based on the whitelist data from [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist).
