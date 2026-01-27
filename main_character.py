# main_character.py
import arcade


class SheriffBorya(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.idle_texture = arcade.load_texture("images/sprite.png")
        self.walk_right = arcade.load_texture("images/sprite_right.png")
        self.walk_left = arcade.load_texture("images/sprite_left.png")
        self.walk_up = arcade.load_texture("images/sprite_up.png")
        self.walk_down = arcade.load_texture("images/sprite_down.png")

        self.texture = self.idle_texture
        self.center_x = 300
        self.center_y = 200
        self.change_x = 0
        self.change_y = 0

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x > 0:
            self.texture = self.walk_right
        elif self.change_x < 0:
            self.texture = self.walk_left
        elif self.change_y > 0:
            self.texture = self.walk_up
        elif self.change_y < 0:
            self.texture = self.walk_down
        else:
            self.texture = self.idle_texture

    def move(self, left: bool, right: bool, up: bool, down: bool):
        self.change_x = 0
        self.change_y = 0

        if left:
            self.change_x = -self.speed
        if right:
            self.change_x = self.speed
        if up:
            self.change_y = self.speed
        if down:
            self.change_y = -self.speed
