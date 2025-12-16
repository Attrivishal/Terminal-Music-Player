import pygame # type: ignore
import os
import sys
import time

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.playing = False
        self.volume = 0.8
        self.current_song = None
    
    def play_song(self, song_path):
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.playing = True
            self.current_song = os.path.basename(song_path)
            
            print(f"\n▶️  PLAYING: {self.current_song}")
            print(f"🔊 Volume: {int(self.volume*100)}%")
            self.show_controls()
            
            # Control loop
            self.control_loop()
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_controls(self):
        print("\n🎮 CONTROLS:")
        print("  [SPACE]  Play/Pause")
        print("  [S]      Stop")
        print("  [+]      Volume Up")
        print("  [-]      Volume Down")
        print("  [Q]      Quit")
        print("-" * 30)
    
    def control_loop(self):
        while True:
            if pygame.mixer.music.get_busy():
                # Show playing status
                print(f"\r♫ Now Playing: {self.current_song[:30]:30} | Press SPACE to pause", end="", flush=True)
            else:
                if self.playing:
                    print(f"\n✅ Song finished!")
                    break
            
            # Check for key press (non-blocking)
            try:
                import select
                import tty
                import termios
                
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                
                try:
                    tty.setraw(fd)
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1)
                        self.handle_key(key)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    
            except:
                # Simple fallback for Windows
                time.sleep(0.1)
    
    def handle_key(self, key):
        key = key.lower()
        
        if key == ' ':  # Space - Play/Pause
            if self.playing:
                pygame.mixer.music.pause()
                self.playing = False
                print(f"\r⏸️  PAUSED: {self.current_song[:30]:30} | Press SPACE to resume")
            else:
                pygame.mixer.music.unpause()
                self.playing = True
                print(f"\r▶️  PLAYING: {self.current_song[:30]:30} | Press SPACE to pause")
        
        elif key == 's':  # Stop
            pygame.mixer.music.stop()
            self.playing = False
            print(f"\n⏹️  STOPPED")
            return 'stop'
        
        elif key == '+':  # Volume Up
            self.volume = min(1.0, self.volume + 0.1)
            pygame.mixer.music.set_volume(self.volume)
            print(f"\r🔊 Volume: {int(self.volume*100)}%", end="")
        
        elif key == '-':  # Volume Down
            self.volume = max(0.0, self.volume - 0.1)
            pygame.mixer.music.set_volume(self.volume)
            print(f"\r🔉 Volume: {int(self.volume*100)}%", end="")
        
        elif key == 'q':  # Quit
            pygame.mixer.music.stop()
            print(f"\n👋 GOODBYE!")
            return 'quit'
        
        return None

def main():
    print("=" * 50)
    print("🎵 ADVANCED MUSIC PLAYER")
    print("=" * 50)
    
    player = MusicPlayer()
    
    # List available songs
    music_folder = "music"
    if not os.path.exists(music_folder):
        print(f"❌ Folder '{music_folder}' not found!")
        return
    
    songs = [f for f in os.listdir(music_folder) if f.lower().endswith('.mp3')]
    
    if not songs:
        print("❌ No MP3 files found!")
        return
    
    print(f"\n📀 Available Songs ({len(songs)}):")
    for i, song in enumerate(songs, 1):
        print(f"  {i}. {song}")
    
    # Select song
    try:
        choice = int(input(f"\n🎯 Select song (1-{len(songs)}): "))
        if 1 <= choice <= len(songs):
            song_path = os.path.join(music_folder, songs[choice-1])
        else:
            print("❌ Invalid choice!")
            return
    except:
        print("❌ Please enter a valid number!")
        return
    
    # Play the song
    player.play_song(song_path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Player closed by user")
    finally:
        pygame.mixer.quit()