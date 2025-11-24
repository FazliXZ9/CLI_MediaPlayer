import pygame
import os
import time
import threading
from datetime import datetime

START_TIME = "06:50"
END_TIME   = "15:40"

command = None
running = True

def is_active_hours():
    now = datetime.now().time()
    start = datetime.strptime(START_TIME, "%H:%M").time()
    end = datetime.strptime(END_TIME, "%H:%M").time()
    
    return start <= now <= end

def input_listener():
    global command, running
    while running:
        try:
            user_input = input().strip().lower()
            if user_input in ['n', 'b', 'q', 'next', 'back', 'quit']:
                command = user_input
                pygame.mixer.music.stop() 
            if user_input == 'q':
                break
        except:
            break

def main():
    global command, running
    
    pygame.mixer.init(frequency=44100)
    music_dir = "."
    
    playlist = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
    playlist.sort()

    if not playlist:
        print("Tidak ada file MP3!")
        return

    print(f"Sistem Siap. Jadwal Aktif: {START_TIME} s/d {END_TIME}")
    print(f"Total Lagu: {len(playlist)}")
    print("------------------------------------------------")
    print("KONTROL (Ketik lalu tekan Enter):")
    print("  [n] Next  -> Lagu Selanjutnya")
    print("  [b] Back  -> Lagu Sebelumnya")
    print("  [q] Quit  -> Keluar")
    print("------------------------------------------------\n")

    t = threading.Thread(target=input_listener)
    t.daemon = True
    t.start()

    index = 0
    total_songs = len(playlist)

    try:
        while running:
            if not is_active_hours():
                if pygame.mixer.music.get_busy():
                    print("\nWaktu habis (Di luar jam kerja). Mematikan musik...")
                    pygame.mixer.music.stop()
                
                time.sleep(30)
                continue 

            song = playlist[index]
            song_path = os.path.join(music_dir, song)
            
            if not pygame.mixer.music.get_busy():
                print(f"\n[{datetime.now().strftime('%H:%M')}] ▶️  Memutar: {song}")
                try:
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"Error: {e}")
                    index = (index + 1) % total_songs

            while pygame.mixer.music.get_busy() and command is None:
                if not is_active_hours():
                    pygame.mixer.music.stop()
                    break 
                time.sleep(0.5)

            if command == 'q':
                running = False
                break
            elif command in ['n', 'next']:
                print(" ⏭Skip")
                index = (index + 1) % total_songs
                command = None
            elif command in ['b', 'back']:
                print(" ⏮Prev")
                index = (index - 1 + total_songs) % total_songs
                command = None
            else:
                if is_active_hours():
                    index = (index + 1) % total_songs

    except KeyboardInterrupt:
        print("\nForce Quit.")

if __name__ == "__main__":
    main()