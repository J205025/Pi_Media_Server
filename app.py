# app.py
import os
import random
import subprocess
import threading
import vlc
from flask import Flask, jsonify, render_template, request, session, redirect, url_for, g
from flask_apscheduler import APScheduler
from flask_session import Session
import config

# --- Classes for State Management ---

class MusicLibrary:
    """Manages the music file library."""
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.file_list = []
        self.base_folders = self._get_subdirectories(self.base_dir)

    def _get_subdirectories(self, folder_path):
        """Scans and returns immediate subdirectories."""
        try:
            return [d.name for d in os.scandir(folder_path) if d.is_dir()]
        except FileNotFoundError:
            return []

    def get_artist_list(self, music_type):
        """Gets subdirectories for a given music type."""
        path = os.path.join(self.base_dir, music_type)
        return self._get_subdirectories(path)

    def scan_directory(self, subdirectory=""):
        """
        Scans a subdirectory for media files and updates the file list.
        Recognizes mp3, flac, and ape files.
        """
        songs = []
        full_scan_path = os.path.join(self.base_dir, subdirectory)

        for path, _, files in os.walk(full_scan_path):
            relative_path = os.path.relpath(path, self.base_dir)
            if relative_path == ".":
                relative_path = ""
            
            for file in files:
                if file.lower().endswith(('.mp3', '.flac', '.ape')):
                    songs.append(os.path.join(relative_path, file))
        
        songs.sort()
        self.file_list = songs
        return self.file_list

class PlayerManager:
    """Manages VLC player instances and playback state."""
    def __init__(self, music_library):
        self.library = music_library
        
        # VLC setup
        self.vlc_instance = vlc.Instance(config.VLC_OPTIONS)
        self.music_player = self.vlc_instance.media_player_new()
        self.radio_player = self.vlc_instance.media_player_new()
        
        # State
        self.current_index = 0
        self.is_playing_music = False
        self.active_radio_url = None
        self.volume = config.DEFAULT_VOLUME
        self.is_muted = False
        self.play_mode = config.DEFAULT_PLAY_MODE
        self.play_rate = 1.0
        
        # Event handling for end of track
        events = self.music_player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.handle_end_of_track)

    def handle_end_of_track(self, event):
        """Callback for when a music track finishes."""
        if self.is_playing_music:
            self.next_track()

    def play_music(self, index=None):
        """Plays a music file from the library."""
        if not self.library.file_list:
            return

        if index is not None:
            self.current_index = index
        
        self.stop_radio()
        
        file_path = os.path.join(self.library.base_dir, self.library.file_list[self.current_index])
        media = self.vlc_instance.media_new(file_path)
        self.music_player.set_media(media)
        self.music_player.play()
        self.is_playing_music = True

    def toggle_pause_music(self):
        """Toggles the pause state for the music player."""
        if self.is_playing_music or self.music_player.get_media() is not None:
            self.music_player.pause()
            self.is_playing_music = self.music_player.get_state() == vlc.State.Playing

    def next_track(self):
        """Plays the next track based on the current play mode."""
        if not self.library.file_list:
            return
        
        max_index = len(self.library.file_list)
        if self.play_mode == config.PLAY_MODE_RANDOM:
            self.current_index = random.randint(0, max_index - 1)
        elif self.play_mode == config.PLAY_MODE_SEQUENTIAL:
            self.current_index = (self.current_index + 1) % max_index
        # For PLAY_MODE_REPEAT_ONE, do nothing to index.
        
        self.play_music()

    def previous_track(self):
        """Plays the previous track."""
        if not self.library.file_list:
            return
            
        max_index = len(self.library.file_list)
        if self.play_mode == config.PLAY_MODE_RANDOM:
            self.current_index = random.randint(0, max_index - 1)
        else: # Sequential or Repeat One
            self.current_index = (self.current_index - 1 + max_index) % max_index
            
        self.play_music()

    def play_radio(self, url):
        """Plays a radio stream from a URL."""
        self.stop_music()
        self.active_radio_url = url
        media = self.vlc_instance.media_new(url)
        self.radio_player.set_media(media)
        self.radio_player.play()

    def stop_radio(self):
        """Stops the radio player."""
        if self.radio_player.is_playing():
            self.radio_player.stop()
        self.active_radio_url = None

    def stop_music(self):
        """Stops the music player."""
        if self.music_player.is_playing():
            self.music_player.stop()
        self.is_playing_music = False

    def adjust_volume(self, amount):
        """Adjusts the volume by a given amount (+/-)."""
        self.set_volume(self.volume + amount)

    def set_volume(self, level):
        """Sets the volume to a specific level (0-100)."""
        self.volume = max(0, min(100, level))
        self.music_player.audio_set_volume(self.volume)
        self.radio_player.audio_set_volume(self.volume)
        self.is_muted = self.volume == 0

    def cycle_play_rate(self):
        """Cycles through playback speeds."""
        rate = self.play_rate + config.RATE_STEP
        if rate > config.MAX_RATE:
            rate = config.MIN_RATE
        self.play_rate = rate
        self.music_player.set_rate(self.play_rate)

    def set_position(self, time_ms):
        """Seeks to a specific time in the music track."""
        if self.music_player.is_seekable():
            self.music_player.set_time(time_ms)
            
    def get_status(self):
        """Returns a dictionary with the current player status."""
        media = self.music_player.get_media()
        duration = media.get_duration() if media else 0
        
        return {
            "fileList": self.library.file_list,
            "baseFolders": self.library.base_folders,
            "currentIndex": self.current_index,
            "isPlayingMusic": self.is_playing_music,
            "activeRadioUrl": self.active_radio_url,
            "volume": self.volume,
            "isMuted": self.is_muted,
            "playMode": self.play_mode,
            "playRate": self.play_rate,
            "duration": duration,
            "currentTime": self.music_player.get_time(),
        }

# --- Podcast Download Management ---
download_process_monitor = None
is_downloading = threading.Event()

def run_podcast_download():
    """Executes the podcast download script in a subprocess."""
    try:
        command = [config.PODCAST_PYTHON_INTERPRETER, config.PODCAST_DOWNLOAD_SCRIPT]
        subprocess.run(command, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error downloading podcasts: {e}")
    finally:
        is_downloading.clear() # Signal that download is finished

# --- Flask Application Setup ---
app = Flask(__name__, template_folder="templates")
app.config.from_mapping(
    SECRET_KEY='a-more-secure-secret-key-is-needed',
    SESSION_PERMANENT=False,
    SESSION_TYPE="filesystem",
    SCHEDULER_API_ENABLED=True
)
Session(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# --- Initialize Core Components ---
library = MusicLibrary(config.MUSIC_DIR)
player = PlayerManager(library)

# --- Initial Load ---
library.scan_directory("國語/張學友") # Load a default directory
if library.file_list:
    player.current_index = random.randint(0, len(library.file_list) - 1)
    # Pre-load the first media without playing
    file_path = os.path.join(library.base_dir, library.file_list[player.current_index])
    player.music_player.set_media(player.vlc_instance.media_new(file_path))


# --- Flask Routes ---

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = next((u for u in config.USERS if u['id'] == user_id), None) if user_id else None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = next((u for u in config.USERS if u['username'] == username), None)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('index.html')

# --- API Endpoints for Player Control ---
@app.route('/api/status', methods=['GET'])
def get_status():
    """Returns the complete current status of the player."""
    return jsonify(player.get_status())

@app.route('/api/play', methods=['POST'])
def play():
    data = request.get_json()
    index = data.get('index')
    player.play_music(index)
    return jsonify(player.get_status())

@app.route('/api/pause', methods=['POST'])
def pause():
    player.toggle_pause_music()
    return jsonify(player.get_status())
    
@app.route('/api/next', methods=['POST'])
def next_track():
    player.next_track()
    return jsonify(player.get_status())

@app.route('/api/previous', methods=['POST'])
def previous_track():
    player.previous_track()
    return jsonify(player.get_status())

@app.route('/api/volume', methods=['POST'])
def set_volume():
    data = request.get_json()
    if 'level' in data:
        player.set_volume(int(data['level']))
    if 'adjust' in data:
        player.adjust_volume(int(data['adjust']))
    return jsonify(player.get_status())

@app.route('/api/play_mode', methods=['POST'])
def set_play_mode():
    data = request.get_json()
    player.play_mode = int(data['mode'])
    return jsonify(player.get_status())

@app.route('/api/play_rate', methods=['POST'])
def cycle_play_rate():
    player.cycle_play_rate()
    return jsonify(player.get_status())

@app.route('/api/seek', methods=['POST'])
def seek():
    data = request.get_json()
    player.set_position(int(data['time']) * 1000) # Convert seconds to ms
    return jsonify(player.get_status())
    
@app.route('/api/play_radio', methods=['POST'])
def play_radio():
    data = request.get_json()
    radio_id = str(data.get('radio_id'))
    if radio_id == "0":
        player.stop_radio()
    elif radio_id in config.RADIO_URLS:
        player.play_radio(config.RADIO_URLS[radio_id])
    return jsonify(player.get_status())
    
@app.route('/api/library/scan', methods=['POST'])
def scan_library():
    data = request.get_json()
    music_type = data.get('music_type', '')
    artist = data.get('artist', '')
    subdirectory = os.path.join(music_type, artist)
    library.scan_directory(subdirectory)
    player.stop_music() # Stop playback when library changes
    return jsonify(player.get_status())

@app.route('/api/library/artists', methods=['POST'])
def get_artists():
    data = request.get_json()
    music_type = data.get('music_type')
    if not music_type:
        return jsonify({"error": "music_type is required"}), 400
    return jsonify({"artists": library.get_artist_list(music_type)})
    
@app.route('/api/podcast/download', methods=['POST'])
def download_podcast():
    """Triggers the podcast download script."""
    if is_downloading.is_set():
        return jsonify({"status": "already_running", "message": "Podcast download is already in progress."}), 429
    
    is_downloading.set()
    download_thread = threading.Thread(target=run_podcast_download)
    download_thread.start()
    
    return jsonify({"status": "started", "message": "Podcast download has started."})

# --- Scheduled Jobs ---
@scheduler.task('cron', id='daily_podcast_download', day='*', hour=6, minute=0)
def scheduled_podcast_job():
    """Scheduled job to download podcasts daily."""
    print("Executing scheduled podcast download.")
    if not is_downloading.is_set():
        is_downloading.set()
        run_podcast_download()
        
# A simple example of a scheduled player action
# @scheduler.task('cron', id='play_morning_music', hour=7, minute=30)
# def play_morning_music():
#     """Example: play a specific song at 7:30 AM."""
#     library.scan_directory("Classical")
#     player.play_music(index=0)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE, threaded=config.THREADED_MODE)
