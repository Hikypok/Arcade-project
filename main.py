# main.py
import arcade
from login_view import LoginView


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(1000, 700, "Хроники участкового")
        self.player_id = None
        self.player_name = None
        self.music = None
        self.music_player = None
        
    def play_menu_music(self):
        if self.music_player is None:
            self.music = arcade.Sound("sounds/menu_sound.mp3")
            self.music_player = self.music.play(loop=True, volume=0.5)

    def stop_menu_music(self):
        if self.music_player:
            self.music_player.pause()
            self.music_player.delete()
            self.music_player = None


def main():
    window = GameWindow()
    login_view = LoginView()
    window.show_view(login_view)
    arcade.run()


if __name__ == "__main__":
    main()