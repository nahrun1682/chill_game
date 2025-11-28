"""ゲーム設定管理"""


class Config:
    """ゲームの設定を管理するシングルトン風クラス"""

    def __init__(self):
        # 波の設定
        self.wave_interval = 120  # フレーム（30fps）: 120 = 4秒
        self.wave_interval_min = 60   # 2秒
        self.wave_interval_max = 300  # 10秒
        self.wave_interval_step = 30  # 1秒刻み

        self.wave_reach = 50  # 波の到達距離
        self.wave_reach_min = 20
        self.wave_reach_max = 80
        self.wave_reach_step = 10

        self.wave_power = 50  # 砂を流す強さ（%）
        self.wave_power_min = 10
        self.wave_power_max = 100
        self.wave_power_step = 10

        # 砂の設定
        self.sand_amount = 3  # 1フレームあたりの砂粒数
        self.sand_amount_min = 1
        self.sand_amount_max = 10
        self.sand_amount_step = 1

        # 水の設定
        self.water_amount = 3  # 1フレームあたりの水粒数
        self.water_amount_min = 1
        self.water_amount_max = 10
        self.water_amount_step = 1

        # 音の設定
        self.bgm_on = True
        self.se_on = True

    def get_wave_interval_sec(self) -> float:
        """波の間隔を秒で返す"""
        return self.wave_interval / 30

    def get_wave_power_ratio(self) -> float:
        """波の強さを0-1の比率で返す"""
        return self.wave_power / 100


# グローバル設定インスタンス
config = Config()
