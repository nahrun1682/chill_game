"""海と波の描画"""
import pyxel
import math
import random


class Sea:
    def __init__(self, y_start: int, height: int, beach_y: int):
        self.y_start = y_start
        self.height = height
        self.beach_y = beach_y  # 砂浜の開始位置
        self.wave_offset = 0.0

        # 大波（砂を流す波）
        self.big_wave_active = False
        self.big_wave_y = 0  # 波の現在位置
        self.big_wave_max_y = beach_y + 20  # 波が届く最大位置
        self.big_wave_timer = 0
        self.big_wave_interval = 180  # 約6秒ごと（30fps）
        self.big_wave_speed = 0.5
        self.big_wave_returning = False  # 波が戻ってるか

    def update(self):
        # 波のアニメーション用オフセット
        self.wave_offset += 0.05

        # 大波タイマー
        self.big_wave_timer += 1
        if not self.big_wave_active and self.big_wave_timer >= self.big_wave_interval:
            self.big_wave_active = True
            self.big_wave_y = self.beach_y
            self.big_wave_returning = False
            self.big_wave_timer = 0

        # 大波の動き
        if self.big_wave_active:
            if not self.big_wave_returning:
                # 波が進む
                self.big_wave_y += self.big_wave_speed
                if self.big_wave_y >= self.big_wave_max_y:
                    self.big_wave_returning = True
            else:
                # 波が戻る
                self.big_wave_y -= self.big_wave_speed * 0.7
                if self.big_wave_y <= self.beach_y:
                    self.big_wave_active = False

    def get_wave_zone(self) -> tuple[bool, int]:
        """大波が砂に触れてるか、どこまで来てるか"""
        if self.big_wave_active:
            return True, int(self.big_wave_y)
        return False, 0

    def draw(self):
        # 海の基本色（濃い青）
        pyxel.rect(0, self.y_start, pyxel.width, self.height, 1)

        # 波のライン（明るい青でゆらゆら）
        for i in range(3):
            y = self.y_start + 2 + i * 4
            for x in range(0, pyxel.width, 2):
                wave_y = y + int(math.sin(x * 0.1 + self.wave_offset + i) * 1.5)
                pyxel.pset(x, wave_y, 12)  # 明るい青
                pyxel.pset(x + 1, wave_y, 12)

        # 大波の描画
        if self.big_wave_active:
            wave_y = int(self.big_wave_y)
            # 波の泡（白いライン）
            for x in range(pyxel.width):
                wobble = int(math.sin(x * 0.3 + self.wave_offset * 2) * 2)
                pyxel.pset(x, wave_y + wobble, 7)  # 白
                if random.random() < 0.3:
                    pyxel.pset(x, wave_y + wobble - 1, 12)  # 明るい青
