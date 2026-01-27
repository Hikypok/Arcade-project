# dialog_system.py
import arcade


class DialogueBox:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.visible = False
        self.lines = []
        self.speaker = ""
        self.on_close = None

    def show(self, speaker, text, on_close=None):
        self.speaker = speaker
        max_width = self.window_width - 80
        self.lines = self._split_text(text, max_width)
        self.visible = True
        self.on_close = on_close

    def _split_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) * 8 > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return lines

    def draw(self):
        if not self.visible:
            return

        width = self.window_width - 60
        height = 150
        x = 50
        y = 50

        arcade.draw_rect_filled(
            arcade.rect.LBWH(x, y, width, height),
            color=arcade.color.GRAY_ASPARAGUS)
        arcade.draw_rect_outline(
            arcade.rect.LBWH(x, y, width, height),
            color=arcade.color.WHITE,
            border_width=3)

        if self.speaker:
            arcade.draw_text(
                f"{self.speaker}:",
                x + 20,
                y + height - 40,
                arcade.color.YELLOW,
                16,
                bold=True)

        text_y = y + height - 60
        for line in self.lines:
            arcade.draw_text(
                line,
                x + 20,
                text_y,
                arcade.color.WHITE,
                14)
            text_y -= 20

        arcade.draw_text(
            "[Нажмите SPACE, чтобы продолжить]",
            x + width // 2 - 120,
            y + 15,
            arcade.color.ASH_GREY,
            12)

    def close(self):
        self.visible = False
        if self.on_close:
            self.on_close()

