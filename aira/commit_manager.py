# aira/commit_manager.py
class CommitManager:
    def __init__(self, config):
        self.config = config

    # 今後のフェーズで実装するメソッド
    def create_commit_message(self, changes, llm_client):
        pass

    def stage_files(self):
        pass

    def commit(self):
        pass