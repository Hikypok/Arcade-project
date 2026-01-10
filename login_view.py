import arcade
from arcade import gui
from database import get_or_create_player


class LoginView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture("images/login_menu_bg.jpg")

        self.input_field = gui.UIInputText(text="", width=320, height=45, font_size=18)
        self.input_field.center_x = self.window.width // 2
        self.input_field.center_y = self.window.height // 2

        login_button = gui.UIFlatButton(text="Продолжить", width=200, height=45, font_size=18)
        login_button.center_x = self.window.width // 2
        login_button.center_y = self.window.height // 2 - 70
        login_button.on_click = lambda event: self._try_login()

        self.manager.add(self.input_field)
        self.manager.add(login_button)

    def _try_login(self):
        name = self.input_field.text.strip()
        if not name:
            return

        player_id = get_or_create_player(name)
        self.window.player_id = player_id
        self.window.player_name = name
        from main_menu_view import MainMenuView
        menu_view = MainMenuView()
        self.window.show_view(menu_view)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self._try_login()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(self.window.width // 2,
                                                  self.window.height // 2,
                                                  self.window.width, self.window.height))
        arcade.draw_text("Представьтесь, товарищ участковый:",
                         self.window.width // 2,
                         self.window.height // 2 + 50,
                         arcade.color.WHITE,
                         font_size=35,
                         anchor_x="center")
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()
