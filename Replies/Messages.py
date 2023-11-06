"""
Base language module in Traditional Chinese
"""


class Messages:
    # Generic system messages
    KEYWORD_REPLY_ENABLED = "✅ 已為**{}**開啟關鍵字回覆。"
    KEYWORD_REPLY_DISABLED = "✅ 已為**{}**關閉關鍵字回覆。"

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

    # Jukebox messages
    JUKEBOX_JOIN = ":white_check_mark: 已加入語音頻道：**{}**。" # 指令已綁定至此頻道。"
    JUKEBOX_LEAVE = ":arrow_left: 已解除連接。"
    JUKEBOX_NO_VOICE_CHANNEL = ":question: 我不知道你在哪裡QQ"
    JUKEBOX_ALREADY_CONNECTED = ":question: 我已經加入語音頻道囉？"
    JUKEBOX_SEARCHING = ":mag: 正在搜尋：`{}`"
    JUKEBOX_NO_MATCHES = ":x: 搜尋結果為空。"
    JUKEBOX_SKIPPED = ":track_next: 跳過！"
    JUKEBOX_LOOP_ONE_DISABLED_AUTO = ":arrow_right: 已自動停用單曲循環播放。"
    JUKEBOX_NO_MORE_SONGS = ":warning: 沒歌了！使用`{}play`加入更多歌曲。"
    JUKEBOX_IMPORTED_PLAYLIST = ":white_check_mark: 已從播放清單匯入**{}**首歌曲。"
    JUKEBOX_PLAYLIST_PRIVATE = ":warning: 此播放清單可能為私人清單。"
    JUKEBOX_STREAM_WARNING = ":information_source: 播放中的歌曲為直播，可使用`{}skip`跳過。"
    JUKEBOX_PLAYLIST_INFO = ":information_source: 如要匯入完整清單，請在`{}play`後方貼上：{}"
    JUKEBOX_SONG_REMOVED = ":white_check_mark: 已移除歌曲：**{}**"
    JUKEBOX_AUTOPLAY_ENABLED = ":information_source: 已啟用自動播放。將在播放清單結束後自動播放推薦歌曲。"
    JUKEBOX_AUTOPLAY_DISABLED = ":information_source: 已停用自動播放。"