import arcade
from arcade import gui
from database import is_level_completed


class LevelsMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture("images/levels_menu_bg.jpg")

        self.return_main_menu = gui.UIFlatButton(text="Вернуться в главное меню", width=500, height=60, font_size=30)
        self.return_main_menu.center_x = self.window.width // 2
        self.return_main_menu.center_y = self.window.height // 2 - 200
        self.return_main_menu.on_click = lambda event: self._return_main_menu()

        self.level1 = gui.UIFlatButton(text=f"Уровень 1", width=150, height=150, font_size=60)
        self.level1.center_x = 100
        self.level1.center_y = 600
        self.level1.on_click = lambda event: self._start_level(1)

        self.level2 = gui.UIFlatButton(text=f"Уровень 2", width=150, height=150, font_size=60)
        self.level2.center_x = 300
        self.level2.center_y = 600
        self.level2.on_click = lambda event: self._start_level(2)

        self.level3 = gui.UIFlatButton(text=f"Уровень 3", width=150, height=150, font_size=60)
        self.level3.center_x = 500
        self.level3.center_y = 600
        self.level3.on_click = lambda event: self._start_level(3)

        self.level4 = gui.UIFlatButton(text=f"Уровень 4", width=150, height=150, font_size=60)
        self.level4.center_x = 700
        self.level4.center_y = 600
        self.level4.on_click = lambda event: self._start_level(4)

        self.level5 = gui.UIFlatButton(text=f"Уровень 5", width=150, height=150, font_size=60)
        self.level5.center_x = 900
        self.level5.center_y = 600
        self.level5.on_click = lambda event: self._start_level(5)

        self.manager.add(self.return_main_menu)
        self.manager.add(self.level1)
        self.manager.add(self.level2)
        self.manager.add(self.level3)
        self.manager.add(self.level4)
        self.manager.add(self.level5)

        self._update_level_access()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(self.window.width // 2,
                                                  self.window.height // 2,
                                                  self.window.width, self.window.height))
        self.manager.draw()

    def _update_level_access(self):
        player_id = self.window.player_id
        self.level1.disabled = False
        self.level2.disabled = not is_level_completed(player_id, "level_1")
        self.level3.disabled = not is_level_completed(player_id, "level_2")
        self.level4.disabled = not is_level_completed(player_id, "level_3")
        self.level5.disabled = not is_level_completed(player_id, "level_4")

    def _return_main_menu(self):
        from main_menu_view import MainMenuView
        self.window.show_view(MainMenuView())

    def _start_level(self, level_num: int):
        player_id = self.window.player_id
        level_id = f"level_{level_num}"
        if level_num == 1:
            allowed = True
        else:
            allowed = is_level_completed(player_id, f"level_{level_num - 1}")
        if not allowed:
            return
        from database import unlock_level
        unlock_level(player_id, f"level_{level_num}")  # ВРЕМЕННО! УДАЛИ ЭТО ПОЗЖН ОБЯЗАТЕЛЬНО!!
        self._update_level_access()  # ВРЕМЕННО! УДАЛИ ЭТО ПОЗЖЕ ОБЯЗАТЕЛЬНО
        if level_num == 1:
            from levels.level1_view import Level1View
            self.window.stop_menu_music()
            self.window.show_view(Level1View())
        elif level_num == 2:
            from levels.level2_view import Level2View
            self.window.stop_menu_music()
            self.window.show_view(Level2View())
        elif level_num == 3:
            from levels.level3_view import Level3View
            self.window.stop_menu_music()
            self.window.show_view(Level3View())
        elif level_num == 4:
            from levels.level4_view import Level4View
            self.window.stop_menu_music()
            self.window.show_view(Level4View())
        elif level_num == 5:
            from levels.level5_view import Level5View
            self.window.stop_menu_music()
            self.window.show_view(Level5View())


