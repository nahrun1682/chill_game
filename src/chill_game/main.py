"""
砂浜シミュレーター - Chill Beach
チルい砂遊びゲーム
"""
import pyxel
import random
from sand import SandSimulator
from sea import Sea


class ChillBeach:
    def __init__(self):
        # 画面サイズ 128x128 (レトロ感)
        pyxel.init(128, 128, title="Chill Beach", fps=30)

        # レイアウト
        self.sky_height = 40
        self.sea_height = 25
        self.beach_y = self.sky_height + self.sea_height  # 砂浜開始位置

        # コンポーネント
        self.sea = Sea(self.sky_height, self.sea_height, self.beach_y)
        self.sand = SandSimulator(self.beach_y)

        # 波が戻った時に貝殻を置くフラグ
        self.wave_was_returning = False

        # ゲーム開始
        pyxel.run(self.update, self.draw)

    def update(self):
        # ESCで終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # スペースで砂の色切り替え
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.sand.cycle_color()

        # マウスクリック/ドラッグで砂を落とす
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            # 複数粒落とす
            for _ in range(3):
                offset_x = random.randint(-2, 2)
                self.sand.add_sand(mx + offset_x, my)

        # 更新
        self.sea.update()

        # 波が砂を流す処理
        wave_active, wave_y = self.sea.get_wave_zone()
        if wave_active:
            self.sand.wave_wash(wave_y, self.sea.big_wave_returning)

            # 波が戻り始めた瞬間に貝殻を置く
            if self.sea.big_wave_returning and not self.wave_was_returning:
                if random.random() < 0.7:  # 70%の確率で貝殻
                    shell_x = random.randint(10, 118)
                    shell_y = random.randint(self.beach_y + 2, self.beach_y + 18)
                    self.sand.add_shell(shell_x, shell_y)

            self.wave_was_returning = self.sea.big_wave_returning
        else:
            self.wave_was_returning = False

        self.sand.update()

    def draw(self):
        # 空（グラデーション風）
        pyxel.cls(12)  # 明るい青
        for y in range(self.sky_height):
            # 上が濃く、下が明るい
            if y < 15:
                pyxel.line(0, y, 127, y, 1)  # 濃い青
            elif y < 30:
                pyxel.line(0, y, 127, y, 5)  # 紫がかった青

        # 太陽
        pyxel.circ(100, 15, 8, 10)  # 黄色
        pyxel.circ(100, 15, 6, 9)   # オレンジ

        # 海
        self.sea.draw()

        # 砂浜の背景（ベースの砂色）
        pyxel.rect(0, self.beach_y, 128, 128 - self.beach_y, 15)  # ベージュ

        # 波が来てる部分は水色で塗る
        wave_active, wave_y = self.sea.get_wave_zone()
        if wave_active:
            wave_height = wave_y - self.beach_y
            if wave_height > 0:
                pyxel.rect(0, self.beach_y, 128, wave_height, 12)  # 明るい青

        # 砂
        self.sand.draw()

        # UI
        pyxel.text(2, 2, "CHILL BEACH", 7)
        pyxel.text(2, 120, "[SPACE]:COLOR [Q]:QUIT", 7)


if __name__ == "__main__":
    ChillBeach()
