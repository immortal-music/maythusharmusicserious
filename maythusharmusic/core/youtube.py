import os
import re
import random
import asyncio
from pathlib import Path
from typing import Optional, Union

import yt_dlp
from py_yt import VideosSearch
from pyrogram import enums, types

from maythusharmusic.helpers import Track, utils


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.cookies = []
        self.checked = False
        self.regex = r"(https?://)?(www\.|m\.)?(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})"

    def get_cookies(self):
        if not self.checked:
            for file in os.listdir("maythusharmusic/cookies"):
                if file.endswith(".txt"):
                    self.cookies.append(file)
            self.checked = True
        if not self.cookies:
            return None
        return f"maythusharmusic/cookies/{random.choice(self.cookies)}"

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    def url(self, message_1: types.Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            text = message.text or message.caption or ""

            if message.entities:
                for entity in message.entities:
                    if entity.type == enums.MessageEntityType.URL:
                        return text[entity.offset : entity.offset + entity.length]

            if message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == enums.MessageEntityType.TEXT_LINK:
                        return entity.url

        return None

    async def search(self, query: str, m_id: int, video: bool = False) -> Track | None:
        _search = VideosSearch(query, limit=1)
        results = await _search.next()
        if results and results["result"]:
            data = results["result"][0]
            return Track(
                id=data.get("id"),
                channel_name=data.get("channel", {}).get("name"),
                duration=data.get("duration"),
                duration_sec=utils.to_seconds(data.get("duration")),
                message_id=m_id,
                title=data.get("title")[:25],
                thumbnail=data.get("thumbnails", [{}])[-1].get("url").split("?")[0],
                url=data.get("link"),
                view_count=data.get("viewCount", {}).get("short"),
                video=video,
            )
        return None

    async def download(self, video_id: str, video: bool = False) -> Optional[str]:
        url = self.base + video_id
        
        # Audio အတွက် m4a ကို default ထားပြီး၊ filename ကို yt-dlp ကနေတဆင့် သတ်မှတ်မယ်
        ext = "mp4" if video else "m4a"
        filename = f"downloads/{video_id}.{ext}"

        if Path(filename).exists():
            return filename

        base_opts = {
            "outtmpl": filename,  # output template ကို filename အတိုင်း အတိအကျ သတ်မှတ်
            "quiet": True,
            "noplaylist": True,
            "geo_bypass": True,
            "no_warnings": True,
            "overwrites": False,
            "ignoreerrors": True, # Error ကို python exception မတက်အောင် လုပ်ထား
            "nocheckcertificate": True,
            "cookiefile": self.get_cookies(),
        }

        if video:
            ydl_opts = {
                **base_opts,
                # Video format ကို ပို flexible ဖြစ်အောင်ပြင်
                "format": "bestvideo[ext=mp4][height<=?720]+bestaudio[ext=m4a]/best[ext=mp4][height<=?720]/best",
            }
        else:
            ydl_opts = {
                **base_opts,
                # Audio format ကို ပို flexible ဖြစ်အောင်ပြင်
                "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
                "postprocessors": [{ # Audio file သီးသန့်ဖြစ်အောင် m4a ကို extract လုပ်
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
            }

        def _download():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Download လုပ်ပြီးနောက် ဖိုင်တကယ်ရှိမရှိ စစ်ဆေး
                if Path(filename).exists():
                    return filename
                else:
                    # Download လုပ်တာ မအောင်မြင်ခဲ့ရင် (Format error, etc.)
                    return None
            except Exception:
                # တခြား မမျှော်လင့်ထားတဲ့ error တက်ရင်
                return None

        return await asyncio.to_thread(_download)

