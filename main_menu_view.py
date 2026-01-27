# main_menu_view.py
import arcade
from arcade import gui


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture("images/main_menu_bg.jpg")

        self.change_user_button = gui.UIFlatButton(text="Сменить Участкового", width=500, height=60, font_size=30)
        self.change_user_button.center_x = self.window.width // 2
        self.change_user_button.center_y = self.window.height // 2 + 100
        self.change_user_button.on_click = lambda event: self._change_user()

        self.levels_menu_button = gui.UIFlatButton(text="Меню выбора уровней", width=500, height=60, font_size=30)
        self.levels_menu_button.center_x = self.window.width // 2
        self.levels_menu_button.center_y = self.window.height // 2 + 30
        self.levels_menu_button.on_click = lambda event: self._go_to_levels()

        self.exit_button = gui.UIFlatButton(text="Выйти из игры", width=500, height=60, font_size=30)
        self.exit_button.center_x = self.window.width // 2
        self.exit_button.center_y = self.window.height // 2 - 40
        self.exit_button.on_click = lambda event: self._exit_game()

        self.manager.add(self.change_user_button)
        self.manager.add(self.levels_menu_button)
        self.manager.add(self.exit_button)

        self.window.play_menu_music()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(self.window.width // 2,
                                                  self.window.height // 2,
                                                  self.window.width, self.window.height))
        self.manager.draw()

    def _change_user(self):
        from login_view import LoginView
        self.window.stop_menu_music()
        self.window.show_view(LoginView())

    def _go_to_levels(self):
        from levels_menu_view import LevelsMenuView
        self.window.show_view(LevelsMenuView())

    def _exit_game(self):
        arcade.close_window()
