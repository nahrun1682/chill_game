"""
砂浜シミュレーター - Chill Beach
チルい砂遊びゲーム
"""
import pyxel
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
        self.sea = Sea(self.sky_height, self.sea_height)
        self.sand = SandSimulator(self.beach_y)

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
                import random
                offset_x = random.randint(-2, 2)
                self.sand.add_sand(mx + offset_x, my)

        # 更新
        self.sea.update()
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

        # 砂
        self.sand.draw()

        # UI
        pyxel.text(2, 2, "CHILL BEACH", 7)
        pyxel.text(2, 120, "[SPACE]:COLOR [Q]:QUIT", 7)


if __name__ == "__main__":
    ChillBeach()
