# level2_view.py
import arcade
from arcade.camera import Camera2D
from main_character import SheriffBorya
from dialog_system import DialogueBox


class Level2View(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.sheriff = SheriffBorya()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.keys = set()
        self.found_clues = set()

        self.clue_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.has_basement_key = False
        self.has_shown_entrance_dialog = False
        self._exiting = False

        self.bg_sound = None
        self.bg_sound_player = None

        self.dialogue_box = None
        self.show_interact_hint = False

        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

        self.level_width = 2700
        self.level_height = 1350
        self.setup()

    def setup(self):
        self.background = arcade.load_texture("images/house_level2.png")
        self.bg_sound = arcade.Sound("sounds/Diablo_bg_sound.mp3")
        self.bg_sound_player = self.bg_sound.play(loop=True, volume=0.3)
        self.sheriff.scale = 0.7
        self.player_list.append(self.sheriff)
        self.sheriff.center_x = 160
        self.sheriff.center_y = 460

        w, h = self.window.width, self.window.height
        self.world_camera.viewport = arcade.rect.XYWH(w / 2, h / 2, w, h)
        self.gui_camera.viewport = arcade.rect.XYWH(w / 2, h / 2, w, h)
        self.world_camera.zoom = 2.0

        # стены и мебель
        wall_left1 = arcade.SpriteSolidColor(20, 350, arcade.color.BLACK)
        wall_left1.center_x = 80
        wall_left1.center_y = 400
        self.wall_list.append(wall_left1)

        wall_up = arcade.SpriteSolidColor(700, 30, arcade.color.BLACK)
        wall_up.center_x = 400
        wall_up.center_y = 535
        self.wall_list.append(wall_up)

        wall_right_1 = arcade.SpriteSolidColor(20, 200, arcade.color.BLACK)
        wall_right_1.center_x = 700
        wall_right_1.center_y = 430
        self.wall_list.append(wall_right_1)

        kitchen_wall = arcade.SpriteSolidColor(50, 60, arcade.color.BLACK)
        kitchen_wall.center_x = 650
        kitchen_wall.center_y = 355
        self.wall_list.append(kitchen_wall)

        wall_right_2 = arcade.SpriteSolidColor(20, 300, arcade.color.BLACK)
        wall_right_2.center_x = 775
        wall_right_2.center_y = 230
        self.wall_list.append(wall_right_2)

        kitchen_wall = arcade.SpriteSolidColor(50, 60, arcade.color.BLACK)
        kitchen_wall.center_x = 735
        kitchen_wall.center_y = 365
        self.wall_list.append(kitchen_wall)

        wall_down2 = arcade.SpriteSolidColor(250, 20, arcade.color.BLACK)
        wall_down2.center_x = 640
        wall_down2.center_y = 80
        self.wall_list.append(wall_down2)

        wall_kitchen_table1 = arcade.SpriteSolidColor(140, 75, arcade.color.BLACK)
        wall_kitchen_table1.center_x = 697
        wall_kitchen_table1.center_y = 108
        self.wall_list.append(wall_kitchen_table1)

        wall_middle2 = arcade.SpriteSolidColor(200, 40, arcade.color.BLACK)
        wall_middle2.center_x = 450
        wall_middle2.center_y = 365
        self.wall_list.append(wall_middle2)

        wall_middle3 = arcade.SpriteSolidColor(3, 250, arcade.color.BLACK)
        wall_middle3.center_x = 505
        wall_middle3.center_y = 260
        self.wall_list.append(wall_middle3)

        wall_down_left = arcade.SpriteSolidColor(150, 10, arcade.color.BLACK)
        wall_down_left.center_x = 150
        wall_down_left.center_y = 290
        self.wall_list.append(wall_down_left)

        wall_left2 = arcade.SpriteSolidColor(5, 250, arcade.color.BLACK)
        wall_left2.center_x = 225
        wall_left2.center_y = 260
        self.wall_list.append(wall_left2)

        wall_middle1 = arcade.SpriteSolidColor(60, 40, arcade.color.BLACK)
        wall_middle1.center_x = 260
        wall_middle1.center_y = 365
        self.wall_list.append(wall_middle1)

        wall_down1 = arcade.SpriteSolidColor(200, 10, arcade.color.BLACK)
        wall_down1.center_x = 340
        wall_down1.center_y = 140
        self.wall_list.append(wall_down1)

        wall_telek = arcade.SpriteSolidColor(50, 30, arcade.color.BLACK)
        wall_telek.center_x = 380
        wall_telek.center_y = 180
        self.wall_list.append(wall_telek)

        wall_table1 = arcade.SpriteSolidColor(45, 20, arcade.color.BLACK)
        wall_table1.center_x = 255
        wall_table1.center_y = 230
        self.wall_list.append(wall_table1)

        wall_celar1 = arcade.SpriteSolidColor(100, 5, arcade.color.BLACK)
        wall_celar1.center_x = 440
        wall_celar1.center_y = 60
        self.wall_list.append(wall_celar1)

        wall_celar2 = arcade.SpriteSolidColor(5, 80, arcade.color.BLACK)
        wall_celar2.center_x = 410
        wall_celar2.center_y = 80
        self.wall_list.append(wall_celar2)

        # улики и их "стены"
        table_wall = arcade.SpriteSolidColor(45, 20, arcade.color.BLACK)
        table_wall.center_x = 450
        table_wall.center_y = 330
        self.wall_list.append(table_wall)

        table_clue = arcade.SpriteSolidColor(60, 35, arcade.color.BLACK)
        table_clue.center_x = 450
        table_clue.center_y = 330
        table_clue.properties = {"action": "table"}
        self.clue_list.append(table_clue)

        bag_wall = arcade.SpriteSolidColor(20, 20, arcade.color.BLACK)
        bag_wall.center_x = 202
        bag_wall.center_y = 320
        self.wall_list.append(bag_wall)

        bag_clue = arcade.SpriteSolidColor(35, 35, arcade.color.BLACK)
        bag_clue.center_x = 202
        bag_clue.center_y = 320
        bag_clue.properties = {"action": "bags"}
        self.clue_list.append(bag_clue)

        kitchen_table_wall = arcade.SpriteSolidColor(50, 60, arcade.color.BLACK)
        kitchen_table_wall.center_x = 535
        kitchen_table_wall.center_y = 205
        self.wall_list.append(kitchen_table_wall)

        kitchen_table_clue = arcade.SpriteSolidColor(65, 75, arcade.color.BLACK)
        kitchen_table_clue.center_x = 535
        kitchen_table_clue.center_y = 205
        kitchen_table_clue.properties = {"action": "kitchen_table"}
        self.clue_list.append(kitchen_table_clue)

        wardrop_wall = arcade.SpriteSolidColor(50, 30, arcade.color.BLACK)
        wardrop_wall.center_x = 400
        wardrop_wall.center_y = 520
        self.wall_list.append(wardrop_wall)

        wardrop_clue = arcade.SpriteSolidColor(65, 45, arcade.color.BLACK)
        wardrop_clue.center_x = 400
        wardrop_clue.center_y = 520
        wardrop_clue.properties = {"action": "closet"}
        self.clue_list.append(wardrop_clue)

        mirror = arcade.SpriteSolidColor(20, 70, arcade.color.BLACK)
        mirror.center_x = 200
        mirror.center_y = 470
        mirror.properties = {"action": "broken_mirror"}
        self.clue_list.append(mirror)

        key_clue = arcade.SpriteSolidColor(120, 15, arcade.color.GOLD)
        key_clue.center_x = 670
        key_clue.center_y = 100
        key_clue.properties = {"action": "basement_key"}
        self.clue_list.append(key_clue)

        door = arcade.Sprite("images/door_level2.png", scale=0.2)
        door.center_x = 440
        door.center_y = 90
        door.properties = {"action": "basement_door"}
        self.door_list.append(door)
        door.center_x, door.center_y = 440, 105
        self.clue_list.append(door)

        self.dialogue_box = DialogueBox(self.window.width, self.window.height)

    def center_camera_to_player(self):
        zoom = self.world_camera.zoom
        half_view_w = (self.window.width / 2) / zoom
        half_view_h = (self.window.height / 2) / zoom

        target_x = self.sheriff.center_x
        target_y = self.sheriff.center_y

        min_x = half_view_w
        max_x = self.level_width - half_view_w
        min_y = half_view_h
        max_y = self.level_height - half_view_h

        clamped_x = max(min_x, min(target_x, max_x))
        clamped_y = max(min_y, min(target_y, max_y))

        self.world_camera.position = (clamped_x, clamped_y)

    def on_draw(self):
        self.clear()
        with self.world_camera.activate():
            if self.background:
                arcade.draw_texture_rect(
                    self.background,
                    arcade.rect.XYWH(
                        self.window.width // 2,
                        self.window.height // 2,
                        self.window.width,
                        self.window.height
                    )
                )
            self.door_list.draw()
            self.player_list.draw()
            with self.gui_camera.activate():
                if self.show_interact_hint:
                    arcade.draw_text(
                        "Для взаимодействия используйте кнопку E.",
                        20,
                        self.window.height - 30,
                        arcade.color.WHITE,
                        16,
                        bold=True
                    )
                arcade.draw_text(
                    "Для выхода в меню уровней используйте ESC",
                    20,
                    10,
                    arcade.color.WHITE,
                    16
                )
                self.dialogue_box.draw()

    def on_update(self, delta_time):
        if self.dialogue_box and self.dialogue_box.visible:
            return

        start_x = self.sheriff.center_x
        start_y = self.sheriff.center_y

        left = arcade.key.LEFT in self.keys or arcade.key.A in self.keys
        right = arcade.key.RIGHT in self.keys or arcade.key.D in self.keys
        up = arcade.key.UP in self.keys or arcade.key.W in self.keys
        down = arcade.key.DOWN in self.keys or arcade.key.S in self.keys

        self.sheriff.move(left, right, up, down)

        self.sheriff.center_x += self.sheriff.change_x
        if arcade.check_for_collision_with_list(self.sheriff, self.wall_list):
            self.sheriff.center_x = start_x

        self.sheriff.center_y += self.sheriff.change_y
        if arcade.check_for_collision_with_list(self.sheriff, self.wall_list):
            self.sheriff.center_y = start_y

        if arcade.check_for_collision_with_list(self.sheriff, self.clue_list):
            self.show_interact_hint = True
        else:
            self.show_interact_hint = False

        self.sheriff.update_animation(delta_time)
        self.center_camera_to_player()

        if not self.has_shown_entrance_dialog:
            self._show_entrance_dialog()
            self.has_shown_entrance_dialog = True
            return

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE and self.dialogue_box.visible:
            self.dialogue_box.close()
            return
        if symbol == arcade.key.ESCAPE:
            self.exit_on_levels_menu()
        if symbol in (
                arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D,
                arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT
        ):
            self.keys.add(symbol)
        elif symbol == arcade.key.E:
            self._check_interaction()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (
                arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D,
                arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.keys.discard(symbol)

    def _check_interaction(self):
        clues_hit = arcade.check_for_collision_with_list(self.sheriff, self.clue_list)
        for clue in clues_hit:
            action = clue.properties.get("action")
            if action in ("bags", "table", "kitchen_table", "closet", "broken_mirror", "basement_key"):
                if action not in self.found_clues:
                    self.found_clues.add(action)
            if action == "bags":
                self._check_bags()
            elif action == "table":
                self._check_table()
            elif action == "kitchen_table":
                self._check_kitchen_table()
            elif action == "closet":
                self._check_closet()
            elif action == "broken_mirror":
                self._check_broken_mirror()
            elif action == "basement_key":
                self.has_basement_key = True
                text = (
                    "Ключ... Спрятан в глиняном горшке.\n"
                    "На нём надпись: «Не открывай. Забудь.»\n"
                    "Кто это писал? Антонина? Или... Лиза?\n"
                    "В любом случае — подвал знает правду.\n"
                    "Ключ у меня! Значит, пора отправляться вниз")
                self.dialogue_box.show("Боря", text)
            elif action == "basement_door":
                self._try_open_basement()

            break

    def _check_bags(self):
        text = ("Чемодан распахнут... Всё готово к отъезду.\n"
                "Билеты на поезд — завтра утром. И пачка денег — свежие купюры.\n"
                "Но если она боялась недоброжелателя, зачем оставлять билеты на виду?\n"
                "Странно... Как будто кто-то *хочет*, чтобы мы нашли этот чемодан.")
        self.dialogue_box.show("Боря", text)

    def _check_kitchen_table(self):
        text = ("Чайник ещё тёплый. А рядом — два стакана.\n"
                "Кофеёк это тема, конечно. Я бы сам не отказался сейчас...\n"
                "Антонина Крейн — одинокая женщина. И у неё нет ни детей, ни семьи.\n"
                "Неужели кто-то ещё здесь живёт... Но кто? Почему? Зачем?...\n"
                "Эта женщина очень вряд-ли живет с парнем...")
        self.dialogue_box.show("Боря", text)

    def _check_broken_mirror(self):
        text = ("Зеркало разбито... Но странно — осколки все внутрь комнаты.\n"
                "Если бы ударили в ярости — стекло летело бы во все стороны.\n"
                "А тут аккуратно, будто... специально.\n"
                "\n"
                "И кровь?.. Скорее всего, купленная в театральной лавке.\n"
                "Всё это — спектакль. Кто-то хочет, чтобы мы думали: здесь было насилие.\n"
                "Но зачем?.. Чтобы скрыть бегство? Или... отвлечь от чего-то?")
        self.dialogue_box.show("Боря", text)

    def _check_closet(self):
        text = ("Шкаф забит до отказа! Платья, пальто, сумки... На десятерых хватит.\n"
                "И все — разных стилей: строгие костюмы, яркие платья, даже детская куртка...\n"
                "Странно для одинокой писательницы. Как будто здесь живут две женщины.\n"
                "\n"
                "А вот и записка, смятая в уголке:\n"
                "'Помогите. Мне очень плохо. Моя сестра держит меня в подвале.\n"
                "Она заставляет меня писать. Я не хочу... Я устала...\n"
                "Запасной ключ от подвала должен быть в одном из цветочных горшков"
                "\n"
                "Сестра?.. Значит, Антонина — не жертва. А тюремщик.")
        self.dialogue_box.show("Боря", text)

    def _check_table(self):
        text = ("У стола - смятые бумажки. Нервный срыв? Страх кого-то?\n"
                "На столе — договор с издательством. Подпись «Антонина Крейн».\n"
                "Но почерк... дрожащий, неуверенный. Совсем не как на автографах.\n"
                "А если присмотреться — под чернильным пятном проступает имя: Лиза.\n"
                "Выходит, книги писала не она... А славу собирала другая.")
        self.dialogue_box.show("Боря", text)

    def _show_entrance_dialog(self):
        text = (
            "Ну вот и дом Антонины Крейн...\n"
            "Тихо. Слишком тихо.\n"
            "\n"
            "Соседи говорили — она боялась кого-то. Пряталась по ночам.\n"
            "А теперь её нет...\n"
            "\n"
            "Ладно, Боря. Осматривайся. Каждая деталь может быть важна.")
        self.dialogue_box.show("Боря", text)

    def _try_open_basement(self):
        if self.has_basement_key:
            open_sound = arcade.Sound("sounds/door_open.mp3")
            open_sound.play(volume=0.7)
            if self.bg_sound_player:
                self.bg_sound.stop(self.bg_sound_player)
                self.bg_sound_player = None
            if hasattr(self.window, 'player_id') and self.window.player_id:
                from database import unlock_level
                unlock_level(self.window.player_id, "level_2")
            total_found = len(self.found_clues)
            self.window.show_view(Level2CompleteView(total_found))
        else:
            door_sound = arcade.Sound("sounds/door_close.mp3")
            door_sound.play(volume=0.6)
            text = "Дверь заперта. Нужен ключ."
            self.dialogue_box.show("Боря", text)

    def exit_on_levels_menu(self):
        if self._exiting:
            return
        self._exiting = True
        if self.bg_sound_player:
            self.bg_sound.stop(self.bg_sound_player)
            self.bg_sound_player = None

        from levels_menu_view import LevelsMenuView
        self.window.play_menu_music()
        self.window.show_view(LevelsMenuView())


class Level2CompleteView(arcade.View):
    def __init__(self, clues_found=0):
        super().__init__()
        self.clues_found = clues_found

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "РАССЛЕДОВАНИЕ ЗАВЕРШЕНО!",
            self.window.width // 2,
            self.window.height - 50,
            arcade.color.GOLD,
            36,
            anchor_x="center",
            anchor_y="top",
            bold=True
        )

        if self.clues_found >= 6:
            praise = "Вы нашли всё! Ни одна деталь не ускользнула."
        elif self.clues_found >= 4:
            praise = "Отличная работа! Вы собрали почти все улики."
        elif self.clues_found >= 2:
            praise = "Хорошо, но некоторые тайны остались в тени."
        else:
            praise = "Правда скрыта глубже... Нужно смотреть внимательнее."

        text = (
            f"Найдено улик: {self.clues_found} из 6\n"
            f"{praise}\n"
            "\n"
            "Антонина Крейн — не жертва. Она преступница.\n"
            "Её сестра Лиза писала книги, а Антонина — крала славу.\n"
            "\n"
            "Дверь в подвал открыта...\n"
            "Там, внизу, — последняя правда.\n"
            "\n"
            "Но я чувствую: это ещё не конец.\n"
            "Что-то ждёт меня в темноте...\n"
            "\n"
            "— Участковый Боря"
        )

        arcade.draw_text(
            text,
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.WHITE,
            16,
            anchor_x="center",
            anchor_y="top",
            align="center",
            width=self.window.width - 200,
            multiline=True
        )

        arcade.draw_text(
            "[Нажмите ENTER, чтобы вернуться в меню]",
            self.window.width // 2,
            50,
            arcade.color.ASH_GREY,
            14,
            anchor_x="center"
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            from levels_menu_view import LevelsMenuView
            self.window.play_menu_music()
            self.window.show_view(LevelsMenuView())
            self.window.show_view(LevelsMenuView())
