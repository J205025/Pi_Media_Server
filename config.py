# config.py

# --- Application Settings ---
# Directory where music files are stored.
# The original code used './static/assets/'
MUSIC_DIR = "./static/assets/"
HOST = '0.0.0.0'
PORT = 2000
DEBUG_MODE = True
THREADED_MODE = True


# --- User Authentication ---
# In a production environment, use a database and hashed passwords.
USERS = [
    {"id": 1, "username": "jerry", "password": "1234"},
    {"id": 2, "username": "sasa", "password": "1234"},
    {"id": 3, "username": "amy", "password": "1234"},
]

# --- Radio Stream URLs ---
RADIO_URLS = {
    "1": "https://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    "2": "http://stream.live.vc.bbcmedia.co.uk/bbc_london",
    "3": "https://npr-ice.streamguys1.com/live.mp3",
    "4": "https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
    "5": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_five_live",
    "6": "http://stream.live.vc.bbcmedia.co.uk/bbc_asian_network",
    "7": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
    "8": "https://icrt.leanstream.co/ICRTFM-MP3?args=web",
    "9": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_two",
    "10": "http://localhost:8000/stream.ogg",
    "11": "http://onair.family977.com.tw:8000/live.mp3",
    "12": "https://n09.rcs.revma.com/aw9uqyxy2tzuv?rj-ttl=5&rj-tok=AAABhZollCEACdvxzVVN61ARVg",
    "13": "https://n10.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABhZouFPAAQudE3-49-1PFHQ",
    "14": "https://n09.rcs.revma.com/7mnq8rt7k5zuv?rj-ttl=5&rj-tok=AAABhZovh0cASZAucd0xcmxkvQ",
    "15": "https://n11a-eu.rcs.revma.com/em90w4aeewzuv?rj-tok=AAABhZoyef8AtFfbdaYYtKJnaw&rj-ttl=5",
    "16": "https://n07.rcs.revma.com/78fm9wyy2tzuv?rj-ttl=5&rj-tok=AAABhZozdbQAkV-tPDO6A5aHag",
    "17": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_three",
    "18": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm",
    "19": "http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
    "30": "http://media-ice.musicradio.com:80/ClassicFMMP3"
}

# --- Podcast Settings ---
PODCAST_DOWNLOAD_SCRIPT = "/home/ubuntu/Pi_Media_Server/getpodcast_sh.py"
PODCAST_PYTHON_INTERPRETER = "/home/ubuntu/Pi_Media_Server/.venv/bin/python3"

# --- VLC Settings ---
# Options for VLC instance, e.g., for ALSA audio on Raspberry Pi
VLC_OPTIONS = "--aout=alsa --alsa-audio-device=hw --verbose=-1"

# --- Playback Constants ---
PLAY_MODE_SEQUENTIAL = 0
PLAY_MODE_RANDOM = 1
PLAY_MODE_REPEAT_ONE = 2

DEFAULT_PLAY_MODE = PLAY_MODE_RANDOM
DEFAULT_VOLUME = 65
MIN_RATE, MAX_RATE, RATE_STEP = 0.5, 2.5, 0.25
