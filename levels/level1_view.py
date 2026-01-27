import arcade
from main_character import SheriffBorya
import random
from dialog_system import DialogueBox


class Level1View(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.sheriff = SheriffBorya()
        self.walls_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.keys = set()
        self.rain_emitter = None
        self.rain_drops = []
        self.rain_sound = None
        self.rain_sound_player = None
        self.clue_sprites = arcade.SpriteList()
        self.has_key = False
        self.dialog = DialogueBox(self.window.width, self.window.height)
        self.bag_on_ground = None
        self.show_interact_hint = False

    def setup(self):
        self.background = arcade.load_texture("images/bg_start_level.png")
        self.rain_sound = arcade.Sound("sounds/rain_sound.mp3")
        self.rain_sound_player = self.rain_sound.play(loop=True, volume=0.3)

        house = arcade.SpriteSolidColor(480, 230, arcade.color.BLACK)
        house.center_x, house.center_y = 550, 580
        self.walls_list.append(house)

        tree1 = arcade.SpriteSolidColor(150, 190, arcade.color.BLACK)
        tree1.center_x, tree1.center_y = 950, 580
        self.walls_list.append(tree1)

        tree2 = arcade.SpriteSolidColor(150, 170, arcade.color.BLACK)
        tree2.center_x, tree2.center_y = 120, 330
        self.walls_list.append(tree2)

        sky = arcade.SpriteSolidColor(1000, 170, arcade.color.BLACK)
        sky.center_x, sky.center_y = 500, 620
        self.walls_list.append(sky)

        self.door = arcade.SpriteSolidColor(50, 60, arcade.color.BLACK)
        self.door.center_x, self.door.center_y = 650, 450
        self.door.alpha = 0
        self.clue_sprites.append(self.door)

        self.player_list.append(self.sheriff)

        for _ in range(600):
            x = random.randint(0, self.window.width)
            y = random.randint(0, self.window.height)
            speed = random.uniform(5, 10)
            self.rain_drops.append([x, y, speed])

        self.bag = arcade.Sprite("images/bag.png", 0.05)
        self.bag.center_x, self.bag.center_y = 980, 500
        self.bag.name = "bag"
        self.clue_sprites.append(self.bag)

        self.letter = arcade.Sprite("images/letter.png", 0.03)
        self.letter.center_x, self.letter.center_y = 590, 410
        self.letter.name = "letter"
        self.clue_sprites.append(self.letter)

        self.ivan = arcade.Sprite("images/suspect_level1_back.png", 0.7)
        self.ivan.center_x, self.ivan.center_y = 100, 500
        self.ivan.name = "suspect"
        self.clue_sprites.append(self.ivan)

    def on_draw(self):
        self.clear()
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
        self.clue_sprites.draw()
        self.player_list.draw()
        for x, y, _ in self.rain_drops:
            arcade.draw_line(x, y, x, y + 20, arcade.color.BLUE_GRAY, 1)
        if self.show_interact_hint:
            arcade.draw_text(
                "Для взаимодействия используйте кнопку E.",
                20,
                self.window.height - 40,
                arcade.color.WHITE,
                16,
                bold=True
            )
        arcade.draw_text("Для выхода в меню уровней используйте ESC", 550,
                self.window.height - 40,
                arcade.color.WHITE,
                16,
                bold=True)
        self.dialog.draw()

    def on_update(self, delta_time):
        for drop in self.rain_drops:
            drop[1] -= drop[2]
            if drop[1] < 0:
                drop[1] = self.window.height + random.randint(0, 50)
                drop[0] = random.randint(0, self.window.width)

        start_x = self.sheriff.center_x
        start_y = self.sheriff.center_y

        left = arcade.key.LEFT in self.keys or arcade.key.A in self.keys
        right = arcade.key.RIGHT in self.keys or arcade.key.D in self.keys
        up = arcade.key.UP in self.keys or arcade.key.W in self.keys
        down = arcade.key.DOWN in self.keys or arcade.key.S in self.keys

        self.sheriff.move(left, right, up, down)

        self.sheriff.center_x += self.sheriff.change_x
        if arcade.check_for_collision_with_list(self.sheriff, self.walls_list):
            self.sheriff.center_x = start_x

        self.sheriff.center_y += self.sheriff.change_y
        if arcade.check_for_collision_with_list(self.sheriff, self.walls_list):
            self.sheriff.center_y = start_y
        self.sheriff.update_animation(delta_time)

        near_any = (
                arcade.check_for_collision(self.sheriff, self.ivan) or
                arcade.check_for_collision(self.sheriff, self.bag) or
                arcade.check_for_collision(self.sheriff, self.door) or
                arcade.check_for_collision(self.sheriff, self.letter) or
                (hasattr(self, 'bag_on_ground') and self.bag_on_ground and
                 arcade.check_for_collision(self.sheriff, self.bag_on_ground))
        )
        self.show_interact_hint = near_any

        if arcade.key.E in self.keys:
            if arcade.check_for_collision(self.sheriff, self.letter):
                self._read_letter()
            if self.bag in self.clue_sprites:
                if arcade.check_for_collision(self.sheriff, self.bag):
                    self.dialog.show("Борис Ренатович\n",
                                     "Рыбьи головешки\n! "
                                     "Неужели это сумка Антонины?.. О нет. Мой рост — 172,\n"
                                     "а эта ветка — для баскетболистов. Придётся искать помощь… или лестницу.\n"
                                     "Пока осмотрюсь")
        if arcade.check_for_collision_with_list(self.sheriff, self.walls_list):
            self.sheriff.center_x = start_x
            self.sheriff.center_y = start_y

        self.sheriff.center_x = max(self.sheriff.width / 3,
                                    min(self.sheriff.center_x, self.window.width - self.sheriff.width / 3))
        self.sheriff.center_y = max(self.sheriff.height / 3,
                                    min(self.sheriff.center_y, self.window.height - self.sheriff.height / 3))

    def on_key_press(self, key, modifiers):
        self.keys.add(key)
        if key == arcade.key.SPACE and self.dialog.visible:
            self.dialog.close()

        if key == arcade.key.E:
            if arcade.check_for_collision(self.sheriff, self.door):
                if self.has_key:
                    self._enter_house()
                else:
                    self._try_door_without_key()

            elif arcade.check_for_collision(self.sheriff, self.ivan) and not self.has_key:
                self.start_ivan_dialog()
            elif self.bag_on_ground and arcade.check_for_collision(self.sheriff, self.bag_on_ground):
                self._take_bag()
        if key == arcade.key.ESCAPE:
            self.exit_on_levels_menu()

    def on_key_release(self, key, modifiers):
        if key in self.keys:
            self.keys.remove(key)

    def _read_letter(self):
        self.dialog.show(
            "Письмо",
            "Ты пишешь как инвалид! Твои книги — плагиат!\n"
            "Я читал твои черновики — и знаю, что ты скрываешь.\n"
            "Если не сожжёшь рукопись до завтра — я приду.\n"
            "P.S. Твой \"друг\" из издательства уже всё рассказал.\n"
            "(Подпись: \"Читатель №7\")",
            self.letter_thinkings)

    def letter_thinkings(self):
        self.dialog.show("Борис Ренатович",
                         "Ладно, разберёмся.\n"
                         "Во-первых — угроза реальна. Кто-то читает её черновики.\n"
                         "Во-вторых — \"друг из издательства\" что-то рассказал.\n"
                         "И в-третьих, если он был здесь — возможно, в доме остались следы.\n"
                         "Ордер у меня есть. Пора войти внутрь.", None)

    def exit_on_levels_menu(self):
        self.rain_sound_player.pause()
        self.rain_sound_player.delete()
        from levels_menu_view import LevelsMenuView
        self.window.play_menu_music()
        self.window.show_view(LevelsMenuView())

    def start_ivan_dialog(self):
        self.dialog.show("Боря", "Здравствуйте. Вы местный?", self._ivan1)

    def _ivan1(self):
        self.dialog.show("Иван Петрович", "Ага. Живу тут с рождения. Антонину знаю — тихая, добрая…"
                                          "но странная.", self._ivan2)

    def _ivan2(self):
        self.dialog.show("Боря", "Странная?", self._ivan3)

    def _ivan3(self):
        self.dialog.show(
            "Иван Петрович",
            "Последнее время боялась кого-то. Говорила: “Они читают мои черновики…”.\n"
            "А ещё… вчера кричала ночью. Я выглянул — видел, как кто-то в чёрном убегал от её дома.",
            self._ivan4)

    def _ivan4(self):
        self.dialog.show("Боря", "Вы не вызвали полицию?", self._ivan5)

    def _ivan5(self):
        self.dialog.show("Иван Петрович", "Да я сам из полиции — в отставке. Но… ноги болят, не догнал.", self._ivan6)

    def _ivan6(self):
        self.dialog.show("Боря", "Слушайте… а вы не могли бы достать сумку с дерева?", self._ivan_helps)

    def _ivan_helps(self):
        self.bag.remove_from_sprite_lists()
        self.bag_on_ground = arcade.Sprite("images/bag.png", 0.05)
        self.bag_on_ground.center_x = 980
        self.bag_on_ground.center_y = 400
        self.clue_sprites.append(self.bag_on_ground)
        self.dialog.show("Иван Петрович", "Держите. Высота — не проблема для старого медведя.", None)

    def _take_bag(self):
        self.has_key = True
        self.bag_on_ground.remove_from_sprite_lists()
        self.bag_on_ground = None
        self.dialog.show("", "Ключ от дома! Отлично. Теперь можно и внутрь заглянуть…\n"
                             "Хотя… если там кто-то остался — лучше быть осторожным.")

    def on_show_view(self):
        self.setup()
        self.dialog.show("Борис Ренатович",
                         "Меня, Бориса Ренатовича, снова потревожили. На этот раз — исчезновение писательницы Антонины Крейн.\n"
                         "Говорят, она работала над новым романом… и получала угрозы.\n"
                         "Ордер на обыск у меня есть. Осталось найти ключ, допросить местных — и, может, не утонуть в этой луже под названием \"дело\".\n"
                         "Ладно. Начнём с поиска улик.")

    def _try_door_without_key(self):
        try:
            door_sound = arcade.Sound("sounds/door_close.mp3")
            door_sound.play(volume=0.6)
        except:
            pass

        self.dialog.show(
            "Борис Ренатович",
            "Кхе… заперто. Похоже, мне предстоит найти ключ...\n"
            "Спорим, он в той сумке на дереве? Ха! Если ошибся —\n"
            "придётся выламывать."
        )

    def _enter_house(self):
        try:
            open_sound = arcade.Sound("sounds/door_open.mp3")
            open_sound.play(volume=0.7)
            self.rain_sound_player.pause()
            self.rain_sound_player.delete()
        except:
            pass

        from database import unlock_level
        unlock_level(self.window.player_id, "level_1")

        from levels_menu_view import LevelsMenuView
        self.window.play_menu_music()
        self.window.show_view(LevelsMenuView())
