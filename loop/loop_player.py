import pygame
import os
import time
import threading

command = None
running = True

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
        except EOFError:
            break

def main():
    global command, running
    
    pygame.mixer.init(frequency=44100)
    music_dir = "."
    
    playlist = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
    playlist.sort()

    if not playlist:
        print("Tidak ada file MP3 di folder ini!")
        return

    print(f"Ditemukan {len(playlist)} lagu.")
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
            song = playlist[index]
            song_path = os.path.join(music_dir, song)
            
            print(f"\n [{index+1}/{total_songs}] Memutar: {song}")
            print(">> (Ketik n/b/q): ", end="", flush=True)

            try:
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy() and command is None:
                    time.sleep(0.5)
                
                if command in ['n', 'next']:
                    print(" Skip >>")
                    index = (index + 1) % total_songs 
                    command = None 
                    
                elif command in ['b', 'back']:
                    print(" Prev <<")
                    index = (index - 1 + total_songs) % total_songs 
                    command = None 

                elif command in ['q', 'quit']:
                    print("\n Berhenti.")
                    running = False
                    break
             
                else:
                    index = (index + 1) % total_songs

            except Exception as e:
                print(f"Error memutar {song}: {e}")
                index = (index + 1) % total_songs 

    except KeyboardInterrupt:
        print("\nForce Quit.")

if __name__ == "__main__":
    main()