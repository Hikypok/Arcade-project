# level3_view.py
import arcade
from arcade.camera import Camera2D
from main_character import SheriffBorya
from dialog_system import DialogueBox
from arcade.particles import Emitter, EmitInterval, LifetimeParticle
import random
import math
import time


class Level3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.sheriff = SheriffBorya()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.clue_list = arcade.SpriteList()
        self.keys = set()
        self._exiting = False
        self.is_chase_ended = False

        self.girls_list = arcade.SpriteList()

        self.bg_sound = None
        self.bg_sound_player = None

        self.dialogue_box = None
        self.show_interact_hint = False

        self.smoke_emitter = None
        self.is_smoke_active = False
        self.smoke_end_time = 0.0

        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

        self.level_width = 1054
        self.level_height = 2231
        self.setup()

    def setup(self):
        self.background = arcade.load_texture("images/bg_level3.png")
        self.bg_sound = arcade.Sound("sounds/bg_sound_level3.mp3")
        self.bg_sound_player = self.bg_sound.play(loop=True, volume=0.3)
        self.sheriff.scale = 0.7
        self.player_list.append(self.sheriff)
        self.sheriff.center_x = 800
        self.sheriff.center_y = 350

        self.antonina = arcade.Sprite("images/antonina.png", scale=0.25)
        self.antonina.center_x = 400
        self.antonina.center_y = 660
        self.antonina.properties = {"action": "antonina"}
        self.clue_list.append(self.antonina)
        self.girls_list.append(self.antonina)

        self.liza = arcade.Sprite("images/liza_fell.png", scale=1.0)
        self.liza.center_x = 420
        self.liza.center_y = 2000
        self.liza.properties = {"action": "liza"}
        self.clue_list.append(self.liza)
        self.girls_list.append(self.liza)

        self.dialogue_box = DialogueBox(self.window.width, self.window.height)

        w, h = self.window.width, self.window.height
        self.world_camera.viewport = arcade.rect.XYWH(w / 2, h / 2, w, h)
        self.gui_camera.viewport = arcade.rect.XYWH(w / 2, h / 2, w, h)
        self.world_camera.zoom = 2.2

        # УЛИКИ В ПОДВАЛЕ
        # Клетка
        cage_wall = arcade.SpriteSolidColor(80, 80, arcade.color.BLACK)
        cage_wall.center_x, cage_wall.center_y = 550, 350
        self.wall_list.append(cage_wall)

        cage = arcade.SpriteSolidColor(80, 80, arcade.color.BLACK)
        cage.center_x, cage.center_y = 555, 345
        cage.properties = {"action": "cage"}
        self.clue_list.append(cage)

        # Кровь
        blood1 = arcade.SpriteSolidColor(20, 15, arcade.color.BLACK)
        blood1.center_x, blood1.center_y = 580, 260
        blood1.properties = {"action": "blood1"}
        self.clue_list.append(blood1)

        blood2 = arcade.SpriteSolidColor(25, 10, arcade.color.BLACK)
        blood2.center_x, blood2.center_y = 555, 1490
        blood2.properties = {"action": "blood2"}
        self.clue_list.append(blood2)

        # Консервы
        can1 = arcade.SpriteSolidColor(12, 20, arcade.color.BLACK)
        can1.center_x, can1.center_y = 650, 150
        can1.properties = {"action": "can1"}
        self.clue_list.append(can1)

        can2 = arcade.SpriteSolidColor(12, 20, arcade.color.BLACK)
        can2.center_x, can2.center_y = 620, 130
        can2.properties = {"action": "can2"}
        self.clue_list.append(can2)

        # Листки бумаги
        paper1 = arcade.SpriteSolidColor(15, 10, arcade.color.BLACK)
        paper1.center_x, paper1.center_y = 600, 130
        paper1.properties = {"action": "paper1"}
        self.clue_list.append(paper1)

        paper2 = arcade.SpriteSolidColor(15, 10, arcade.color.BLACK)
        paper2.center_x, paper2.center_y = 520, 130
        paper2.properties = {"action": "paper2"}
        self.clue_list.append(paper2)

        # Книги
        book1 = arcade.SpriteSolidColor(25, 15, arcade.color.BLACK)
        book1.center_x, book1.center_y = 727, 160
        book1.properties = {"action": "book1"}
        self.clue_list.append(book1)

        book2 = arcade.SpriteSolidColor(25, 25, arcade.color.BLACK)
        book2.center_x, book2.center_y = 730, 125
        book2.properties = {"action": "book2"}
        self.clue_list .append(book2)

        # Стены
        wall_right1 = arcade.SpriteSolidColor(5, 1000, arcade.color.BLACK)
        wall_right1.center_x, wall_right1.center_y = 860, 600
        self.wall_list.append(wall_right1)

        wall_right2 = arcade.SpriteSolidColor(10, 800, arcade.color.BLACK)
        wall_right2.center_x, wall_right2.center_y = 640, 1700
        self.wall_list.append(wall_right2)

        wall_right3 = arcade.SpriteSolidColor(15, 300, arcade.color.BLACK)
        wall_right3.center_x, wall_right3.center_y = 780, 1250
        self.wall_list.append(wall_right3)

        wall_right4 = arcade.SpriteSolidColor(90, 100, arcade.color.BLACK)
        wall_right4.center_x, wall_right4.center_y = 780, 1050
        self.wall_list.append(wall_right4)

        wall_right5 = arcade.SpriteSolidColor(100, 5, arcade.color.BLACK)
        wall_right5.center_x, wall_right5.center_y = 700, 1350
        self.wall_list.append(wall_right5)

        wall_right6 = arcade.SpriteSolidColor(180, 120, arcade.color.BLACK)
        wall_right6.center_x, wall_right6.center_y = 760, 700
        self.wall_list.append(wall_right6)

        wall_down = arcade.SpriteSolidColor(800, 5, arcade.color.BLACK)
        wall_down.center_x, wall_down.center_y = 520, 80
        self.wall_list.append(wall_down)

        wall_rock = arcade.SpriteSolidColor(20, 40, arcade.color.BLACK)
        wall_rock.center_x, wall_rock.center_y = 790, 180
        self.wall_list.append(wall_rock)

        wall_middle1 = arcade.SpriteSolidColor(5, 130, arcade.color.BLACK)
        wall_middle1.center_x, wall_middle1.center_y = 430, 170
        self.wall_list.append(wall_middle1)

        wall_middle2 = arcade.SpriteSolidColor(140, 5, arcade.color.BLACK)
        wall_middle2.center_x, wall_middle2.center_y = 370, 230
        self.wall_list.append(wall_middle2)

        wall_middle3 = arcade.SpriteSolidColor(5, 130, arcade.color.BLACK)
        wall_middle3.center_x, wall_middle3.center_y = 300, 300
        self.wall_list.append(wall_middle3)

        wall_left1 = arcade.SpriteSolidColor(5, 500, arcade.color.BLACK)
        wall_left1.center_x, wall_left1.center_y = 155, 250
        self.wall_list.append(wall_left1)

        wall_left2 = arcade.SpriteSolidColor(25, 800, arcade.color.BLACK)
        wall_left2.center_x, wall_left2.center_y = 220, 770
        self.wall_list.append(wall_left2)

        wall_left3 = arcade.SpriteSolidColor(45, 1400, arcade.color.BLACK)
        wall_left3.center_x, wall_left3.center_y = 280, 1550
        self.wall_list.append(wall_left3)

        wall_left_middle1 = arcade.SpriteSolidColor(150, 250, arcade.color.BLACK)
        wall_left_middle1.center_x, wall_left_middle1.center_y = 385, 1340
        self.wall_list.append(wall_left_middle1)

        wall_left_middle2 = arcade.SpriteSolidColor(200, 60, arcade.color.BLACK)
        wall_left_middle2.center_x, wall_left_middle2.center_y = 350, 1950
        self.wall_list.append(wall_left_middle2)

        wall_up1 = arcade.SpriteSolidColor(500, 60, arcade.color.BLACK)
        wall_up1.center_x, wall_up1.center_y = 400, 2050
        self.wall_list.append(wall_up1)

        wall_middle = arcade.SpriteSolidColor(350, 20, arcade.color.BLACK)
        wall_middle.center_x, wall_middle.center_y = 600, 1100
        self.wall_list.append(wall_middle)

        wall_middle = arcade.SpriteSolidColor(150, 100, arcade.color.BLACK)
        wall_middle.center_x, wall_middle.center_y = 550, 1760
        self.wall_list.append(wall_middle)

        wall_middle4 = arcade.SpriteSolidColor(30, 400, arcade.color.BLACK)
        wall_middle4.center_x, wall_middle4.center_y = 560, 950
        self.wall_list.append(wall_middle4)

        wall_middle5 = arcade.SpriteSolidColor(150, 140, arcade.color.BLACK)
        wall_middle5.center_x, wall_middle5.center_y = 445, 820
        self.wall_list.append(wall_middle5)

        wall_middle6 = arcade.SpriteSolidColor(150, 80, arcade.color.BLACK)
        wall_middle6.center_x, wall_middle6.center_y = 440, 500
        self.wall_list.append(wall_middle6)

        wall_middle7 = arcade.SpriteSolidColor(350, 10, arcade.color.BLACK)
        wall_middle7.center_x, wall_middle7.center_y = 660, 400
        self.wall_list.append(wall_middle7)

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

        if self.smoke_emitter:
            self.smoke_emitter.update()
            if time.time() >= self.smoke_end_time:
                self.smoke_emitter = None
                self.is_smoke_active = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE and self.dialogue_box.visible:
            self.dialogue_box.close()
            return
        if symbol == arcade.key.ESCAPE:
            self.exit_on_levels_menu()
        if symbol in (
                arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D,
                arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.keys.add(symbol)
        elif symbol == arcade.key.E:
            self._check_interaction()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (
                arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D,
                arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.keys.discard(symbol)

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
                    arcade.rect.LBWH(0, 0, self.level_width, self.level_height)
                )
            if self.smoke_emitter:
                self.smoke_emitter.draw()
            self.player_list.draw()
            self.girls_list.draw()
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

    def _check_interaction(self):
        clues_hit = arcade.check_for_collision_with_list(self.sheriff, self.clue_list)
        for clue in clues_hit:
            action = clue.properties.get("action")
            if action == "cage":
                self._examine_cage()
            elif action == "blood1":
                self._examine_blood1()
            elif action == "paper1":
                self._examine_paper1()
            elif action == "paper2":
                self._examine_paper2()
            elif action == "book1":
                self._examine_book1()
            elif action == "book2":
                self._examine_book2()
            elif action == "can1":
                self._examine_can1()
            elif action == "can2":
                self._examine_can2()
            elif action == "blood2":
                self._examine_blood2()
            elif action == "antonina":
                if self.is_chase_ended:
                    self._final_confrontation()
                else:
                    self._meet_antonina()
            break

    def _meet_antonina(self):
        text = (
            "Антонина Крейн стоит в свете фонарика.\n"
            "Её глаза — холодные. Голос — дрожащий.\n"
            "\n"
            "— Ты всё понял, Боря?\n"
            "— Лиза — гений. Но мир бы её сломал.\n"
            "— Я её защищала. А теперь она хочет уйти...\n"
            "— Этого нельзя допустить."
        )
        self.dialogue_box.show("Антонина", text, on_close=self._antonina_escaping)

    def _final_confrontation(self):
        text = (
            "Антонина стоит над связанной Лизой.\n"
            "В руке — нож. Глаза — полные боли.\n"
            "\n"
            "— Ты всё равно пришёл...\n"
            "— Но теперь слишком поздно..."
        )
        self.dialogue_box.show("Антонина", text, on_close=self._boris_response)

    def _examine_cage(self):
        text = (
            "Ржавая клетка... Цепи на стене.\n"
            "Здесь держали человека. Недавно.\n"
            "Кто это был?.. Лиза?"
        )
        self.dialogue_box.show("Боря", text)

    def _examine_blood1(self):
        text = (
            "Пятна крови... Свежие.\n"
            "Кто-то боролся здесь. Недавно."
        )
        self.dialogue_box.show("Боря", text)

    def _examine_paper1(self):
        text = (
            "Обрывки бумаги... Черновики.\n"
            "На всех — подпись: «Лиза».\n"
            "Антонина крала не только славу..."
        )
        self.dialogue_box.show("Боря", text)

    def _examine_paper2(self):
        text = (
            "Обрывки бумаги... Дрожащим почерком написано:\n"
            "'Помогите. Я тут уже месяц...\n"
            "Как она может меня так держать?.. Сестра...'")
        self.dialogue_box.show("Боря", text)

    def _examine_book1(self):
        text = ("Это не романы. Это крик души, замаскированный под художественную литературу.\n"
                "Текст на первой странице:\n"
                "'Она сказала: „Ты больна. Мир тебя сломает“.'\n"
                "Но я не больна. Я просто хочу выйти на улицу.\n"
                "Увидеть солнце, купить кофе. Сказать здравствуйте незнакомцу.\n"
                "Почему это преступление?' На полях — пометка карандашом:\n"
                "'Если ты читаешь это — значит, она проиграла.\n"
                "Беги. Не верь её словам. Она умеет плакать навзрыд…\n"
                "но никогда не плачет по-настоящему.'")
        self.dialogue_box.show("Боря", text)

    def _examine_book2(self):
        text = ("Кажется, это личный дневник Лизы. Старая тетрадь в клетку,\n"
                "страницы помяты, местами испачканы слезами.\n"
                "Запись №1 (первая): 'Сегодня она сказала: „Ты будешь писать. Я — быть“\n."
                "Я не поняла. Думала, это игра.\n"
                "Теперь я знаю: я — её тень. Её голос. Её руки.\n"
                "А она — моё лицо. Моё имя. Моя клетка.'")
        self.dialogue_box.show("Боря", text)

    def _examine_can1(self):
        text = ("Банки из-под фасоли, тушёнки, горошка.")
        self.dialogue_box.show("Боря", text)

    def _examine_can2(self):
        text = ("Ещё банка. Записка на банке:\n"
                "'Ешь. Ты нужна мне живой. Пока пишешь — жива.\n"
                "Перестанешь — станешь такой же, как консервы:\n"
                "пустой, просроченной, выброшенной.' Подпись: «А.»")
        self.dialogue_box.show("Боря", text)

    def _examine_blood2(self):
        screem_sound = arcade.Sound("sounds/scream.mp3")
        screem_sound.play(volume=0.8)
        text = ("О ужас...Крик Лизы... И снова кровь... Надо торопиться...\n"
                "Эта женщина - сумасшедшая. Надо быть наготове\n"
                "На кону жизнь человека")
        self.dialogue_box.show("Боря", text)

    def _antonina_escaping(self):
        try:
            smoke_sound = arcade.Sound("sounds/smoke_sound.mp3")
            smoke_sound.play(volume=0.8)
        except Exception as e:
            print(f"Звук дымовой шашки не найден: {e}")
        self._create_smoke_effect(self.antonina.center_x, self.antonina.center_y)
        text = (
            "Она бросает что-то на пол — вспышка!\n"
            "Дым заполняет тоннель.\n"
            "\n"
            "— Беги, Боря! Если поймаешь — спасёшь её.\n"
            "Если нет — она умрёт!"
        )
        self.dialogue_box.show("Боря", text, on_close=self._start_chase)

    def _start_chase(self):
        self.is_chase_ended = True
        if hasattr(self, 'antonina'):
            self.antonina.center_x, self.antonina.center_y = 470, 1980
        text = (
            "— Не с места! Я тебя догоню!\n"
            "\n"
            "*Пфууууэ... Дым!*\n"
            "*Кхэ... Кхээ...*\n"
            "\n"
            "Бежим за ней!!!!!!"
        )
        self.dialogue_box.show("Боря", text)

        """# Простая реализация: сразу к финалу (погоня "проиграна" за кадром)
        self._rescue_liza()"""

    def _create_smoke_effect(self, x, y):
        x = self.sheriff.center_x
        y = self.sheriff.center_y + 50
        if hasattr(self, 'smoke_emitter') and self.smoke_emitter:
            self.smoke_emitter = None

        smoke_color = (100, 100, 100, 200)
        smoke_texture = arcade.make_soft_circle_texture(40, smoke_color)

        def particle_factory(emitter):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.0, 0.2)
            change_x = math.cos(angle) * speed
            change_y = math.sin(angle) * speed + 0.1

            return LifetimeParticle(
                filename_or_texture=smoke_texture,
                change_xy=(change_x, change_y),
                lifetime=random.uniform(2.0, 3.0),
                scale=random.uniform(0.8, 1.6),
                change_angle=random.uniform(-0.1, 0.1),
                angle=random.uniform(0, 360),
            )

        self.smoke_emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitInterval(0.01),
            particle_factory=particle_factory
        )
        self.is_smoke_active = True
        self.smoke_end_time = time.time() + 10.0

    def _level3_complete(self):
        if self.bg_sound_player:
            self.bg_sound.stop(self.bg_sound_player)
            self.bg_sound_player = None

        from database import unlock_level
        if hasattr(self.window, 'player_id') and self.window.player_id:
            unlock_level(self.window.player_id, "level_3")
        self.window.show_view(Level3CompleteView())

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

    def _boris_response(self):
        text = (
            "— Хватит, Антонина!\n"
            "— Ты не защищаешь её. Ты убиваешь её душу!\n"
            "— Отпусти... Пока не стало слишком поздно.\n"
            "\n"
            "Антонина замирает. Нож дрожит в её руке.\n"
            "Слёзы катятся по щекам.\n"
            "\n"
            "— Я... я только хотела... чтобы она была в безопасности...\n"
            "\n"
            "Она роняет нож. Лиза свободна."
        )
        self.dialogue_box.show("Боря", text, on_close=self._level3_complete)


class Level3CompleteView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "ДЕЛО ЗАКРЫТО",
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.GOLD,
            36,
            anchor_x="center",
            bold=True
        )

        text = (
            "Антонина Крейн арестована.\n"
            "Лиза свободна.\n"
            "\n"
            "Но в её глазах — не радость, а страх.\n"
            "Потому что правда — это не только свобода.\n"
            "Это ещё и боль.\n"
            "\n"
            "«Она не жертва. Не преступница.\n"
            "Просто сестра, которая не смогла\n"
            "выбрать между любовью и страхом.»\n"
            "\n"
            "— Участковый Боря"
        )

        arcade.draw_text(
            text,
            self.window.width // 2,
            self.window.height // 2 + 40,
            arcade.color.WHITE,
            16,
            anchor_x="center",
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
            self.window.show_view(LevelsMenuView())


