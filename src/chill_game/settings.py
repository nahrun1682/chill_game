"""設定画面"""
import pyxel
from config import config


class SettingsScreen:
    """設定画面のUI"""

    def __init__(self):
        self.items = [
            {"key": "wave_interval", "label": "WAVE FREQ", "unit": "s", "is_toggle": False},
            {"key": "wave_reach", "label": "WAVE REACH", "unit": "px", "is_toggle": False},
            {"key": "wave_power", "label": "WAVE POWER", "unit": "%", "is_toggle": False},
            {"key": "sand_amount", "label": "SAND AMOUNT", "unit": "", "is_toggle": False},
            {"key": "bgm_on", "label": "BGM", "unit": "", "is_toggle": True},
            {"key": "se_on", "label": "SE", "unit": "", "is_toggle": True},
        ]
        self.selected_idx = 0
        self.is_active = False

    def open(self):
        self.is_active = True
        self.selected_idx = 0

    def close(self):
        self.is_active = False

    def update(self) -> bool:
        """更新。Trueを返したら閉じる"""
        if not self.is_active:
            return False

        # ESCまたはSで閉じる
        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_S):
            self.close()
            return True

        # 上下で項目選択
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_idx = (self.selected_idx - 1) % len(self.items)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_idx = (self.selected_idx + 1) % len(self.items)

        # 左右で値変更
        item = self.items[self.selected_idx]
        if item["is_toggle"]:
            # トグル（ON/OFF）
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                current = getattr(config, item["key"])
                setattr(config, item["key"], not current)
        else:
            # 数値
            key = item["key"]
            current = getattr(config, key)
            min_val = getattr(config, f"{key}_min")
            max_val = getattr(config, f"{key}_max")
            step = getattr(config, f"{key}_step")

            if pyxel.btnp(pyxel.KEY_LEFT):
                new_val = max(min_val, current - step)
                setattr(config, key, new_val)
            if pyxel.btnp(pyxel.KEY_RIGHT):
                new_val = min(max_val, current + step)
                setattr(config, key, new_val)

        return False

    def draw(self):
        if not self.is_active:
            return

        # 背景（半透明風）
        pyxel.rect(10, 20, 108, 90, 0)
        pyxel.rectb(10, 20, 108, 90, 7)

        # タイトル
        pyxel.text(45, 25, "SETTINGS", 7)

        # 項目
        y = 38
        for i, item in enumerate(self.items):
            color = 7 if i == self.selected_idx else 5
            cursor = ">" if i == self.selected_idx else " "

            # ラベル
            pyxel.text(14, y, f"{cursor}{item['label']}", color)

            # 値
            if item["is_toggle"]:
                val = getattr(config, item["key"])
                val_str = "ON" if val else "OFF"
                val_color = 11 if val else 8
            else:
                val = getattr(config, item["key"])
                if item["key"] == "wave_interval":
                    val_str = f"{val // 30}{item['unit']}"
                else:
                    val_str = f"{val}{item['unit']}"
                val_color = color

            # バー表示（数値の場合）
            if not item["is_toggle"]:
                key = item["key"]
                min_val = getattr(config, f"{key}_min")
                max_val = getattr(config, f"{key}_max")
                ratio = (val - min_val) / (max_val - min_val)
                bar_width = int(20 * ratio)
                pyxel.rect(75, y, bar_width, 5, 11)
                pyxel.rectb(75, y, 20, 5, color)
                pyxel.text(98, y, val_str, val_color)
            else:
                pyxel.text(75, y, f"[{val_str}]", val_color)

            y += 10

        # 操作説明
        pyxel.text(20, 100, "UP/DOWN:SELECT LEFT/RIGHT:CHANGE", 6)
        pyxel.text(35, 107, "[S]/[ESC]:CLOSE", 6)
