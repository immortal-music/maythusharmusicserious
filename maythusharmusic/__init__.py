import time
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


__version__ = "3.0.1"

from config import Config

config = Config()
config.check()
tasks = []
boot = time.time()

from maythusharmusic.core.bot import Bot
app = Bot()

from maythusharmusic.core.dir import ensure_dirs
ensure_dirs()

from maythusharmusic.core.userbot import Userbot
userbot = Userbot()

from maythusharmusic.core.mongo import MongoDB
db = MongoDB()

from maythusharmusic.core.lang import Language
lang = Language()

from maythusharmusic.core.telegram import Telegram
from maythusharmusic.core.youtube import YouTube
tg = Telegram()
yt = YouTube()

from maythusharmusic.helpers import Queue
queue = Queue()

from maythusharmusic.core.calls import TgCall
cailin = TgCall()
