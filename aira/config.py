# aira/config.py
import yaml

class Config:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            self.config = yaml.safe_load(f)

    def get(self, key, default=None):
        """
        設定値を取得する。
        key: ドット区切りのキー (例: "gaiah.repo.create_repo")
        default: キーが存在しない場合に返すデフォルト値 (省略可)
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            if value is None:
                return default
        return value