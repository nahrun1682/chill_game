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

        # サウンド設定
        self._setup_sounds()

        # レイアウト
        self.sky_height = 40
        self.sea_height = 25
        self.beach_y = self.sky_height + self.sea_height  # 砂浜開始位置

        # コンポーネント
        self.sea = Sea(self.sky_height, self.sea_height, self.beach_y)
        self.sand = SandSimulator(self.beach_y)

        # 波が戻った時に貝殻を置くフラグ
        self.wave_was_returning = False

        # 砂の音タイマー
        self.sand_sound_timer = 0

        # 環境音開始
        pyxel.play(0, 0, loop=True)

        # ゲーム開始
        pyxel.run(self.update, self.draw)

    def _setup_sounds(self):
        """サウンドを設定"""
        # Sound 0: 波の環境音（ループ、ノイズでザザー）
        # 低めのノイズを長く
        pyxel.sounds[0].set(
            notes="c1c1d1d1c1c1d1d1e1e1d1d1c1c1d1d1",  # 低い音程
            tones="nnnnnnnnnnnnnnnn",  # ノイズ
            volumes="32112233321122333211223332112233",  # 緩やかに上下
            effects="nnnnnnnnnnnnnnnn",
            speed=30  # ゆっくり
        )

        # Sound 1: 大波（ザバーン！）
        pyxel.sounds[1].set(
            notes="c2d2e2f2g2a2b2c3",  # 上昇する音程
            tones="nnnnnnnn",  # ノイズ
            volumes="77665544",  # フェードアウト
            effects="nnnnnnnn",
            speed=8  # 速め
        )

        # Sound 2: 砂を落とす音（サラサラ）
        pyxel.sounds[2].set(
            notes="g3f3e3d3",  # 下降
            tones="nnnn",  # ノイズ
            volumes="3210",  # すぐフェードアウト
            effects="nnnn",
            speed=15  # 短い
        )

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

            # 砂の音（連続再生しすぎないように）
            self.sand_sound_timer += 1
            if self.sand_sound_timer >= 5:  # 5フレームごと
                pyxel.play(2, 2)
                self.sand_sound_timer = 0
        else:
            self.sand_sound_timer = 0

        # 更新
        self.sea.update()

        # 大波が来た瞬間に音
        if self.sea.big_wave_just_started:
            pyxel.play(1, 1)

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
