import arcade
from database import unlock_level


class Level1View(arcade.View):
    def __init__(self):
        super().__init__()
        # тут будут фон, спрайты и нач сост
        self.background = arcade.load_texture("images/bg_level1.png")
        self.message = "Уровень 1: Поймай воришку!"
        self.completed = False

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(self.window.width // 2, self.window.height // 2,
                             self.window.width, self.window.height))
        arcade.draw_text(self.message,
                         self.window.width // 2,
                         self.window.height - 50,
                         arcade.color.WHITE,
                         font_size=24,
                         anchor_x="center")
        arcade.draw_text("Поймай преступника!",
                         self.window.width // 2,
                         50,
                         arcade.color.YELLOW,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE and not self.completed:
            self._complete_level()

    def _complete_level(self):
        if not self.completed:
            self.completed = True
            unlock_level(self.window.player_id, "level_1")
            from levels_menu_view import LevelsMenuView
            self.window.show_view(LevelsMenuView())
