import os
import time
import threading
import subprocess
import signal
from datetime import datetime

# --- KONFIGURASI ---
START_TIME = "07:00"
END_TIME   = "19:30"

MPG123_CMD = ["mpg123", "-r", "48000", "-b", "4096", "-q"] 

music_dir  = "." 

command = None
running = True
current_process = None

def is_active_hours():
    now = datetime.now().time()
    start = datetime.strptime(START_TIME, "%H:%M").time()
    end = datetime.strptime(END_TIME, "%H:%M").time()
    return start <= now <= end

def stop_music():

    global current_process
    if current_process:
        try:
  
            os.kill(current_process.pid, signal.SIGTERM)
            current_process.wait()
        except:
            pass
        current_process = None

def play_music(filepath):
  
    global current_process
    stop_music() 
    
    cmd = MPG123_CMD + [filepath]
    current_process = subprocess.Popen(cmd)

def is_playing():

    global current_process
    if current_process is None:
        return False
    
    return current_process.poll() is None

def input_listener():
    global command, running
    while running:
        try:
            user_input = input().strip().lower()
            if user_input in ['n', 'b', 'q']:
                command = user_input
                stop_music() 
            if user_input == 'q':
                break
        except:
            break

def main():
    global command, running
    
    print("Menggunakan Engine: MPG123")
    
    # --- SCANNING ---
    playlist = []
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith('.mp3'):
                playlist.append(os.path.join(root, file))
    playlist.sort()

    if not playlist:
        print("Tidak ada file MP3!")
        return

    print(f"Sistem Siap. Jadwal: {START_TIME} - {END_TIME}")
    print(f"Total Lagu: {len(playlist)}")
    print("------------------------------------------------")
    
    t = threading.Thread(target=input_listener)
    t.daemon = True
    t.start()

    index = 0
    total_songs = len(playlist)

    try:
        while running:
            
            if not is_active_hours():
                if is_playing():
                    print("\n Jam kerja usai. Musik berhenti.")
                    stop_music()
                time.sleep(30)
                continue

            song_full_path = playlist[index]
            song_name = os.path.basename(song_full_path)
            
            if not is_playing():
                print(f"\n[{datetime.now().strftime('%H:%M')}] Memutar: {song_name}")
                play_music(song_full_path)

            while is_playing() and command is None:
                if not is_active_hours():
                    stop_music()
                    break
                time.sleep(0.5)

            if command == 'q':
                running = False
                stop_music()
                break
            elif command == 'n':
                print(" ⏭️ Skip")
                index = (index + 1) % total_songs
                command = None
            elif command == 'b':
                print(" ⏮️ Prev")
                index = (index - 1 + total_songs) % total_songs
                command = None
            else:
    
                if is_active_hours():
                    index = (index + 1) % total_songs

    except KeyboardInterrupt:
        stop_music()
        print("\nForce Quit.")

if __name__ == "__main__":
    main()
