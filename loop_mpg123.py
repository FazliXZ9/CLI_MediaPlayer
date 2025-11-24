import os
import time
import threading
import subprocess
import signal

# --- KONFIGURASI AUDIO ---
# Kita tetap pakai settingan 'Anti-Keresek' (48kHz + Buffer Besar)
MPG123_CMD = ["mpg123", "-r", "48000", "-b", "4096", "-q"] 

# Direktori Musik (Titik artinya folder saat ini)
music_dir  = "." 

# Variabel Global
command = None
running = True
current_process = None 

def stop_music():
    """Mematikan paksa mpg123"""
    global current_process
    if current_process:
        try:
            os.kill(current_process.pid, signal.SIGTERM)
            current_process.wait()
        except:
            pass
        current_process = None

def play_music(filepath):
    """Menjalankan mpg123 di background"""
    global current_process
    stop_music() # Pastikan yang lama mati dulu
    cmd = MPG123_CMD + [filepath]
    current_process = subprocess.Popen(cmd)

def is_playing():
    """Cek status mpg123"""
    global current_process
    if current_process is None:
        return False
    return current_process.poll() is None

def input_listener():
    """Mendengarkan keyboard user untuk Skip/Back"""
    global command, running
    while running:
        try:
            user_input = input().strip().lower()
            if user_input in ['n', 'b', 'q']:
                command = user_input
                stop_music() # Hentikan lagu agar loop utama lanjut
            if user_input == 'q':
                break
        except:
            break

def main():
    global command, running
    
    print("🔁 Mode: INFINITE LOOP (24 Jam Non-stop)")
    print("🔍 Menggunakan Engine: MPG123 (High Quality)")
    
    # --- SCANNING LAGU (Termasuk Sub-folder) ---
    playlist = []
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith('.mp3'):
                playlist.append(os.path.join(root, file))
    playlist.sort()

    if not playlist:
        print("❌ Tidak ada file MP3!")
        return

    print(f"📂 Total Lagu: {len(playlist)}")
    print("------------------------------------------------")
    print("KONTROL: [n] Next | [b] Back | [q] Quit")
    print("------------------------------------------------")
    
    # Jalankan thread input keyboard
    t = threading.Thread(target=input_listener)
    t.daemon = True
    t.start()

    index = 0
    total_songs = len(playlist)

    try:
        while running:
            song_full_path = playlist[index]
            song_name = os.path.basename(song_full_path)
            
            # Putar Lagu
            if not is_playing():
                print(f"\n▶️  Memutar: {song_name}")
                play_music(song_full_path)

            # TUNGGU LAGU HABIS (Wait Loop)
            # Di sini kita cuma nunggu, tidak perlu cek jam lagi
            while is_playing() and command is None:
                time.sleep(0.5)

            # LOGIKA NAVIGASI (Next/Back/Auto)
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
                # Lagu habis sendiri -> Lanjut lagu berikutnya
                index = (index + 1) % total_songs

    except KeyboardInterrupt:
        stop_music()
        print("\nKeluar.")

if __name__ == "__main__":
    main()
