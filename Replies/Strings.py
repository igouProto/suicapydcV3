"""
Base language module in Traditional Chinese.
Messages contains all the messages Suica would send to the chat.
EmbedStrings contains strings that would appear in embeds.
"""


class Messages:
    # Generic system messages
    BOT_RESTARTING = ":warning: 正在重新啟動..."
    
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
    KEYWORD_REPLY_ENABLED = "✅ 已為**{}**開啟關鍵字回覆。"
    KEYWORD_REPLY_DISABLED = "✅ 已為**{}**關閉關鍵字回覆。"
    KEYWORD_KEY_EXISTS = ':x: 關鍵字已存在。'
    KEYWORD_REPLY_ADDED = ':white_check_mark: 已新增關鍵字：'
    KEYWORD_REPLY_REMOVED = ':white_check_mark: 已移除關鍵字：'
    KEYWORD_KEY_NOT_FOUND = ':x: 找不到關鍵字。'
    KEYWORD_GUILD_NOT_FOUND = ':x: 找不到此伺服器的詞庫。可以使用`{}addkw`新增關鍵字。'
    KEYWORD_REPLY_RELOADED = ':white_check_mark: 匯入詞庫成功。'
    KEYWORD_REPLY_INVALID_FILE = ':x: 詞庫檔案無效。檔名必須為`keywords.txt`。'
    KEYWORD_REPLY_NO_FILE = ':x: 找不到詞庫檔案。'
    KEYWORD_REPLY_MISSING_ARGUMENTS = ':information_source: 指令格式：`{}addkw "關鍵字" "回覆"`'

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
    JUKEBOX_AUTO_DISCONNECTED = "⬅️ 人都跑光光了，那我也要睡啦。"
    JUKEBOX_SEEK = ":mag: 已跳轉至：`{}`"

    # About description template (TODO: This should go to EmbedStrings)
    ABOUT = "ID：{}\n 應用程式名稱：{}\n 擁有者：{}\n 誕生時間：{}\n作者：igouProto [(GitHub!)](https://github.com/igouProto/suicapydcV3)"
    ABOUT_FOOTER = "SUICA v{} • 使用 discord.py 及 wavelink 開發。"
    ABOUT_TITLE = "關於 SUICA"


class EmbedStrings:
    """
    Strings that appears in embeds.
    """
    # Ping
    PING_TITLE = ":clipboard: 西瓜的各種Ping"
    PING_HEARTBEAT = ":heartbeat: Discord WebSocket 延遲"
    PING_REACTIONTIME = ":stopwatch: 指令延遲"
    PING_VOICECLIENT = ":microphone2: 語音延遲"

    # Jukebox
    JUKEBOX_NOTHING_PLAYING = "沒有正在播放的歌曲"
    JUKEBOX_NOTHING_IN_QUEUE = "播放清單為空！"
    JUKEBOX_NOWPLAY_TITLE = "♪ 現正播放"
    JUKEBOX_LOOP_COUNT = "中毒循環中：{}次"
    JUKEBOX_NEW_SONG_ADDED = "♪ {} 已將曲目加入播放清單"
    JUKEBOX_QUEUE_UPNEXT = "接下來"
    JUKEBOX_PAGINATION = "頁數 {}/{}"
    JUKEBOX_QUEUE_UPNEXT_TIME = "總時長 {}"
    JUKEBOX_QUEUE_UPNEXT_COUNT = "共 {} 首"
    JUKEBOX_AUTOPLAY_ENABLED = "已啟用自動播放。將在播放清單結束後自動播放推薦歌曲。"
    JUKEBOX_ERROR_TITLE = ":x: 糟了個糕"
    JUKEBOX_ERROR_DESCRIPTION = "載入曲目時發生錯誤。"
    JUKEBOX_NEW_SONGS_COUNT = "以及其他{}首歌曲。"

    # Omikuji
    OMIKUJI_TITLE = "{} 的每日占卜結果～"
    OMIKUJI_DIRECTION = "歐洲方位"
    OMIKUJI_GACHAINDEX = "抽卡指數"
    OMIKUJI_CHARGEINDEX = "課金指數"
    OMIKUJI_LUCKYNUMBER = "幸運數字"
    OMIKUJI_LUCKYCOLOR = "幸運色"
    OMIKUJI_FOOTER = "天不靈地不理御神籤第{}號。{}"
