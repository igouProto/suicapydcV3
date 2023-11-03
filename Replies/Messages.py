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
