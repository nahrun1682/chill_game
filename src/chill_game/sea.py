"""海と波の描画"""
import pyxel


class Sea:
    def __init__(self, y_start: int, height: int):
        self.y_start = y_start
        self.height = height
        self.wave_offset = 0.0

    def update(self):
        # 波のアニメーション用オフセット
        self.wave_offset += 0.05

    def draw(self):
        # 海の基本色（濃い青）
        pyxel.rect(0, self.y_start, pyxel.width, self.height, 1)

        # 波のライン（明るい青でゆらゆら）
        import math

        for i in range(3):
            y = self.y_start + 2 + i * 4
            for x in range(0, pyxel.width, 2):
                wave_y = y + int(math.sin(x * 0.1 + self.wave_offset + i) * 1.5)
                pyxel.pset(x, wave_y, 12)  # 明るい青
                pyxel.pset(x + 1, wave_y, 12)
