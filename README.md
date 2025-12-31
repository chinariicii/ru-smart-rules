# ru-smart-rules



**🇷🇺 俄罗斯白名单规则转换 (Surge & Loon)**

**🇺🇸 Russian Whitelist Rules Conversion (Surge & Loon)**

**🇷🇺 Преобразование правил белого списка России (Surge & Loon)**




🇨🇳 本项目通过 GitHub Actions 自动抓取上游数据，并转换为适用于 Surge、Loon 等工具的规则列表文件。每天定时自动更新。


🇺🇸 This project automatically fetches data from the upstream whitelist via GitHub Actions and converts it into rule sets for Surge, Loon, and other proxy tools. Updates daily.


🇷🇺 Этот проект автоматически получает данные из исходного "белого списка" через GitHub Actions и преобразует их в наборы правил для Surge, Loon и других прокси-инструментов. Обновляется ежедневно.




---




## 📥 规则订阅 / Subscription/ Подписка


🇨🇳 请根据你的需求选择对应的规则文件链接。

🇺🇸 Select the rule file link according to your needs.

🇷🇺 Выберите ссылку на файл правил в соответствии с вашими потребностями.




| 工具 / Tool / Инструмент | 说明 / Description / Описание | 链接 / Link / Ссылка |
| :--- | :--- | :--- |
| **Surge** | 🇷🇺 俄罗斯常用域名<br>Russian Domains<br>Домены РФ | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/main/dist/surge/ru_whitelist_domains.list` |
| **Surge** | 🇷🇺 俄罗斯 IP 段<br>Russian IPs (CIDR)<br>IP-адреса РФ (CIDR) | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/main/dist/surge/ru_whitelist_cidrs.list` |
| **Loon** | 🇷🇺 俄罗斯常用域名<br>Russian Domains<br>Домены РФ | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/main/dist/loon/ru_whitelist_domains.list` |
| **Loon** | 🇷🇺 俄罗斯 IP 段<br>Russian IPs (CIDR)<br>IP-адреса РФ (CIDR) | `https://raw.githubusercontent.com/chinariicii/ru-smart-rules/main/dist/loon/ru_whitelist_cidrs.list` |




---




## ⚙️ 运行机制 / Workflow / Механизм работы


1. **Trigger / 触发 / Запуск**:
   - 🇨🇳 GitHub Actions 每天定时触发。
   - 🇺🇸 GitHub Actions triggers daily.
   - 🇷🇺 GitHub Actions запускается ежедневно по расписанию.

2. **Fetch / 拉取 / Загрузка**:
   - 🇨🇳 拉取上游最新的 `russia-mobile-internet-whitelist` 数据。
   - 🇺🇸 Fetches the latest data from `russia-mobile-internet-whitelist`.
   - 🇷🇺 Загружает последние данные из `russia-mobile-internet-whitelist`.

3. **Convert / 转换 / Конвертация**:
   - 🇨🇳 通过 Python 脚本转换为 Surge/Loon 格式。
   - 🇺🇸 Converts to Surge/Loon format via Python script.
   - 🇷🇺 Конвертирует в формат Surge/Loon с помощью Python-скрипта.

4. **Push / 推送 / Публикация**:
   - 🇨🇳 自动将生成的规则推送到 `dist` 目录。
   - 🇺🇸 Automatically pushes generated rules to the `dist` directory.
   - 🇷🇺 Автоматически отправляет созданные правила в папку `dist`.




---




## 🔗 Credits / 致谢 / Благодарности

🇨🇳 本项目的规则列表数据来源于 [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist)。
感谢原作者维护的俄罗斯移动网络白名单列表。

🇺🇸 This project generates Surge & Loon rules based on the whitelist data from [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist).
Thanks to the original author for maintaining the Russian mobile internet whitelist.

🇷🇺 Этот проект генерирует правила для Surge и Loon на основе данных "белого списка" из [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist).
Спасибо автору оригинала за поддержку списка разрешенных ресурсов российского мобильного интернета.
