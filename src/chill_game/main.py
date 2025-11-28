"""
砂浜シミュレーター - Chill Beach
チルい砂遊びゲーム
"""
import pyxel
import random
from sand import SandSimulator
from sea import Sea
from config import config
from settings import SettingsScreen


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
        self.settings = SettingsScreen()

        # 音の準備
        self._init_sound()

        # BGM再生開始
        self.bgm_playing = True
        pyxel.playm(0, loop=True)

        # 波が戻った時に貝殻を置くフラグ
        self.wave_was_returning = False

        # ゲーム開始
        pyxel.run(self.update, self.draw)

    def _init_sound(self):
        # BGM: ゆったりとしたメロディ (Track 0)
        pyxel.sound(0).set(
            "c3e3g3b3 c4b3g3e3 a2c3e3g3 a3g3e3c3",
            "t", "4", "n", 24
        )
        # BGM: ベース音 (Track 1)
        pyxel.sound(1).set(
            "c2 r r r f1 r r r",
            "s", "3", "f", 96
        )
        # Music 0 にトラック0と1を割り当て
        pyxel.music(0).set([0], [1], [], [])

        # SE: 砂を置く音 (Sound 2) - ノイズを使って砂っぽい音に
        pyxel.sound(2).set("c2", "n", "2", "f", 3)

        # SE: 大波の音 (Sound 3)
        pyxel.sound(3).set("c2d2e2f2g2", "n", "76543", "n", 8)

    def _update_sound_settings(self):
        """音の設定を反映"""
        # BGM
        if config.bgm_on and not self.bgm_playing:
            pyxel.playm(0, loop=True)
            self.bgm_playing = True
        elif not config.bgm_on and self.bgm_playing:
            pyxel.stop(0)
            pyxel.stop(1)
            self.bgm_playing = False

    def update(self):
        # 設定画面が開いている場合
        if self.settings.is_active:
            self.settings.update()
            self._update_sound_settings()
            # 設定を波に反映
            self.sea.big_wave_interval = config.wave_interval
            self.sea.big_wave_max_y = self.beach_y + config.wave_reach
            return

        # Sキーで設定画面を開く
        if pyxel.btnp(pyxel.KEY_S):
            self.settings.open()
            return

        # Qで終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # スペースで砂の色切り替え
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.sand.cycle_color()

        # マウスクリック/ドラッグで砂を落とす
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y

            # 音を鳴らす (連続しすぎないように少し間引く)
            if config.se_on and pyxel.frame_count % 4 == 0:
                pyxel.play(2, 2)

            # 設定に応じた量の砂を落とす
            for _ in range(config.sand_amount):
                offset_x = random.randint(-2, 2)
                self.sand.add_sand(mx + offset_x, my)

        # 更新
        self.sea.update()

        # 大波が来た瞬間に音
        if self.sea.big_wave_just_started and config.se_on:
            pyxel.play(3, 3)

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
        if not self.settings.is_active:
            pyxel.text(2, 120, "[S]:SETTINGS [SPACE]:COLOR [Q]:QUIT", 6)

        # 設定画面（オーバーレイ）
        self.settings.draw()


if __name__ == "__main__":
    ChillBeach()
