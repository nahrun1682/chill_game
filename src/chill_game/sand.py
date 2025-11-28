"""砂の物理シミュレーション"""
import pyxel
import random
from config import config


class SandParticle:
    def __init__(self, x: int, y: int, color: int = 15):
        self.x = x
        self.y = y
        self.color = color  # 15: 薄いベージュ, 10: 黄色


class Shell:
    """貝殻"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        # 貝殻の種類（見た目のバリエーション）
        self.shell_type = random.randint(0, 2)

    def draw(self):
        # シンプルなドット絵の貝殻
        if self.shell_type == 0:
            # 巻貝風
            pyxel.pset(self.x, self.y, 7)      # 白
            pyxel.pset(self.x + 1, self.y, 6)  # グレー
        elif self.shell_type == 1:
            # 二枚貝風
            pyxel.pset(self.x, self.y, 6)      # グレー
            pyxel.pset(self.x + 1, self.y, 7)  # 白
        else:
            # ピンク貝
            pyxel.pset(self.x, self.y, 14)     # ピンク
            pyxel.pset(self.x + 1, self.y, 7)  # 白


class SandSimulator:
    def __init__(self, beach_y: int):
        self.beach_y = beach_y  # 砂浜の開始Y座標
        self.particles: list[SandParticle] = []
        # 砂のグリッド（Noneか砂粒）
        self.grid: dict[tuple[int, int], SandParticle] = {}
        self.colors = [15, 10, 9]  # ベージュ、黄色、オレンジ
        self.current_color_idx = 0

        # 貝殻
        self.shells: list[Shell] = []

    @property
    def current_color(self) -> int:
        return self.colors[self.current_color_idx]

    def cycle_color(self):
        self.current_color_idx = (self.current_color_idx + 1) % len(self.colors)

    def add_sand(self, x: int, y: int):
        """砂を追加"""
        if y < self.beach_y:
            return  # 海より上には置けない

        if (x, y) in self.grid:
            return  # 既に砂がある

        particle = SandParticle(x, y, self.current_color)
        self.particles.append(particle)
        self.grid[(x, y)] = particle

    def add_shell(self, x: int, y: int):
        """貝殻を追加"""
        # 重ならないようにチェック
        for shell in self.shells:
            if abs(shell.x - x) < 3 and abs(shell.y - y) < 3:
                return
        self.shells.append(Shell(x, y))

    def wave_wash(self, wave_y: int, returning: bool):
        """波が砂を流す"""
        particles_to_move = []
        power = config.get_wave_power_ratio()

        for p in self.particles:
            # 波の位置より上（海側）にある砂だけ影響
            if p.y <= wave_y and p.y >= self.beach_y:
                if returning:
                    # 波が戻るとき：砂を海側（上）に強く引っ張る
                    if random.random() < power:
                        # 1-2ピクセル動かす
                        dy = -random.randint(1, 2)
                        dx = random.randint(-1, 1)
                        particles_to_move.append((p, dx, dy))
                else:
                    # 波が来るとき：砂を横に散らす
                    if random.random() < power * 0.8:
                        dx = random.choice([-2, -1, 1, 2])
                        dy = random.randint(0, 1)
                        particles_to_move.append((p, dx, dy))

        for p, dx, dy in particles_to_move:
            new_x = max(0, min(pyxel.width - 1, p.x + dx))
            new_y = max(self.beach_y, min(pyxel.height - 1, p.y + dy))
            if (new_x, new_y) not in self.grid:
                self._move_particle(p, new_x, new_y)

    def remove_sand_at_top(self):
        """海に入った砂を消す"""
        to_remove = [p for p in self.particles if p.y < self.beach_y]
        for p in to_remove:
            if (p.x, p.y) in self.grid:
                del self.grid[(p.x, p.y)]
            self.particles.remove(p)

    def update(self, water_grid: dict = None):
        """砂の物理更新"""
        if water_grid is None:
            water_grid = {}

        # 下から上に処理（下の砂が先に動く）
        sorted_particles = sorted(self.particles, key=lambda p: -p.y)

        for p in sorted_particles:
            if p.y >= pyxel.height - 1:
                continue  # 画面最下部

            # 下が空いてる？
            below = (p.x, p.y + 1)
            below_left = (p.x - 1, p.y + 1)
            below_right = (p.x + 1, p.y + 1)

            # 砂は他の砂の上には乗れないが、水の上には落ちる
            if below not in self.grid and below[1] < pyxel.height:
                # 真下に落ちる（水の中も通過できる）
                self._move_particle(p, below[0], below[1])
            elif below_left not in self.grid and below_left[0] >= 0 and below_left[1] < pyxel.height:
                # 左下に落ちる
                if random.random() < 0.5:  # ランダム性
                    self._move_particle(p, below_left[0], below_left[1])
            elif below_right not in self.grid and below_right[0] < pyxel.width and below_right[1] < pyxel.height:
                # 右下に落ちる
                if random.random() < 0.5:
                    self._move_particle(p, below_right[0], below_right[1])

        # 海に入った砂を消す
        self.remove_sand_at_top()

    def _move_particle(self, p: SandParticle, new_x: int, new_y: int):
        """パーティクルを移動"""
        del self.grid[(p.x, p.y)]
        p.x = new_x
        p.y = new_y
        self.grid[(p.x, p.y)] = p

    def draw(self):
        """砂を描画"""
        for p in self.particles:
            pyxel.pset(p.x, p.y, p.color)

        # 貝殻を描画
        for shell in self.shells:
            shell.draw()
