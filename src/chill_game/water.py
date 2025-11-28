"""水の流体シミュレーション"""
import pyxel
import random
from config import config


class WaterParticle:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = 12  # 明るい青
        # 少しバリエーション
        if random.random() < 0.3:
            self.color = 1  # 濃い青


class WaterSimulator:
    def __init__(self, beach_y: int):
        self.beach_y = beach_y  # 砂浜の開始Y座標
        self.particles: list[WaterParticle] = []
        # 水のグリッド（Noneか水粒）
        self.grid: dict[tuple[int, int], WaterParticle] = {}

    def add_water(self, x: int, y: int):
        """水を追加"""
        if y < self.beach_y:
            return  # 海より上には置けない

        if (x, y) in self.grid:
            return  # 既に水がある

        particle = WaterParticle(x, y)
        self.particles.append(particle)
        self.grid[(x, y)] = particle

    def is_water_at(self, x: int, y: int) -> bool:
        """指定位置に水があるか"""
        return (x, y) in self.grid

    def is_position_blocked(self, x: int, y: int, sand_grid: dict) -> bool:
        """指定位置が塞がっているか（砂または水）"""
        return (x, y) in self.grid or (x, y) in sand_grid

    def remove_water_at_top(self):
        """海に入った水を消す"""
        to_remove = [p for p in self.particles if p.y < self.beach_y]
        for p in to_remove:
            if (p.x, p.y) in self.grid:
                del self.grid[(p.x, p.y)]
            self.particles.remove(p)

    def update(self, sand_grid: dict, iterations: int = 2):
        """水の物理更新（砂より速く動く）"""
        for _ in range(iterations):
            # 下から上に処理
            sorted_particles = sorted(self.particles, key=lambda p: -p.y)

            for p in sorted_particles:
                self._update_particle(p, sand_grid)

        # 海に入った水を消す
        self.remove_water_at_top()

    def _update_particle(self, p: WaterParticle, sand_grid: dict):
        """1つの水粒子を更新"""
        if p.y >= pyxel.height - 1:
            return  # 画面最下部

        # 下の状態をチェック
        below = (p.x, p.y + 1)
        below_left = (p.x - 1, p.y + 1)
        below_right = (p.x + 1, p.y + 1)

        # 水は砂の下に潜り込もうとする
        if below not in self.grid and below not in sand_grid and below[1] < pyxel.height:
            # 真下に落ちる
            self._move_particle(p, below[0], below[1])
            return

        # 斜め下に移動
        directions = [(below_left, -1), (below_right, 1)]
        random.shuffle(directions)

        for (pos, dx) in directions:
            if pos not in self.grid and pos not in sand_grid and pos[0] >= 0 and pos[0] < pyxel.width and pos[1] < pyxel.height:
                self._move_particle(p, pos[0], pos[1])
                return

        # 下が塞がっている場合、横に広がる（水平になろうとする）
        # 水の特徴：横方向に流れる
        side_dirs = [(-1, 0), (1, 0)]
        random.shuffle(side_dirs)

        for dx, dy in side_dirs:
            new_x = p.x + dx
            new_y = p.y + dy
            if 0 <= new_x < pyxel.width and new_y < pyxel.height:
                if (new_x, new_y) not in self.grid and (new_x, new_y) not in sand_grid:
                    self._move_particle(p, new_x, new_y)
                    return

        # さらに横に2ピクセル流れる（水の広がり）
        if random.random() < 0.3:
            for dx in [-2, 2]:
                new_x = p.x + dx
                if 0 <= new_x < pyxel.width:
                    if (new_x, p.y) not in self.grid and (new_x, p.y) not in sand_grid:
                        self._move_particle(p, new_x, p.y)
                        return

    def _move_particle(self, p: WaterParticle, new_x: int, new_y: int):
        """パーティクルを移動"""
        del self.grid[(p.x, p.y)]
        p.x = new_x
        p.y = new_y
        self.grid[(p.x, p.y)] = p

    def draw(self):
        """水を描画"""
        for p in self.particles:
            pyxel.pset(p.x, p.y, p.color)
