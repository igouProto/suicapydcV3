"""
Base language module in Traditional Chinese
"""


class Messages:
    # Generic system messages
    KEYWORD_REPLY_ENABLED = "已為**{}**開啟關鍵字回覆。"
    KEYWORD_REPLY_DISABLED = "已為**{}**關閉關鍵字回覆。"

    # Admin messages
    EXTENSION_RELOADING = ":warning: 正在重新載入所有模組..."
    EXTENSION_RELOADED = "✅ 已重新載入模組({}/{})。"
    EXTENSION_RELOAD_FAILED = "❌ 重新載入模組失敗：\n{}"
    BOT_BOOTED = "✅ Suica已登入。"

    # Rich presence messages
    DEFAULT_STATUS_MESSAGE = "v{} || {}help"
    PRESENCE_CHANGED = "✅ 已更新狀態訊息至：**{}**"

    # Ping messages
    PINGING = ':stopwatch: 正在測量........'

    # Keyword reply messages
    KEYWORD_KEY_EXISTS = ':x: 關鍵字已存在。'
    KEYWORD_REPLY_ADDED = ':white_check_mark: 已新增關鍵字：'
    KEYWORD_REPLY_REMOVED = ':white_check_mark: 已移除關鍵字：'
    KEYWORD_KEY_NOT_FOUND = ':x: 找不到關鍵字。'
