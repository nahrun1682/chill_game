"""砂の物理シミュレーション"""
import pyxel
import random


class SandParticle:
    def __init__(self, x: int, y: int, color: int = 15):
        self.x = x
        self.y = y
        self.color = color  # 15: 薄いベージュ, 10: 黄色


class SandSimulator:
    def __init__(self, beach_y: int):
        self.beach_y = beach_y  # 砂浜の開始Y座標
        self.particles: list[SandParticle] = []
        # 砂のグリッド（Noneか砂粒）
        self.grid: dict[tuple[int, int], SandParticle] = {}
        self.colors = [15, 10, 9]  # ベージュ、黄色、オレンジ
        self.current_color_idx = 0

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

    def update(self):
        """砂の物理更新"""
        # 下から上に処理（下の砂が先に動く）
        sorted_particles = sorted(self.particles, key=lambda p: -p.y)

        for p in sorted_particles:
            if p.y >= pyxel.height - 1:
                continue  # 画面最下部

            # 下が空いてる？
            below = (p.x, p.y + 1)
            below_left = (p.x - 1, p.y + 1)
            below_right = (p.x + 1, p.y + 1)

            if below not in self.grid and below[1] < pyxel.height:
                # 真下に落ちる
                self._move_particle(p, below[0], below[1])
            elif below_left not in self.grid and below_left[0] >= 0 and below_left[1] < pyxel.height:
                # 左下に落ちる
                if random.random() < 0.5:  # ランダム性
                    self._move_particle(p, below_left[0], below_left[1])
            elif below_right not in self.grid and below_right[0] < pyxel.width and below_right[1] < pyxel.height:
                # 右下に落ちる
                if random.random() < 0.5:
                    self._move_particle(p, below_right[0], below_right[1])

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
