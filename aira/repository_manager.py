# aira/repository_manager.py
import subprocess
from loguru import logger
import os
from gaiah.utils import run_command, tqdm_sleep
from litellm import completion

# import litellm
# litellm.set_verbose=True

class RepositoryManager:
    def __init__(self, config, aira_config):
        self.config = config
        self.aira_config = aira_config

    def is_initialized(self):
        repo_dir = self.config["gaiah"]["local"]["repo_dir"]
        logger.info(f"repo_dir is {repo_dir}")

        # ディレクトリが存在するか確認
        if not os.path.exists(repo_dir):
            return False

        return ".git" in os.listdir(repo_dir)

    def init(self):
        repo_dir = self.config["gaiah"]["local"]["repo_dir"]
        os.makedirs(repo_dir, exist_ok=True)
        run_command(command=["git", "init"], cwd=repo_dir)
        logger.info(f"Initialized repository at {repo_dir}")

    def generate_repository_summary(self, instructions_prompt_path):
        """
        リポジトリの概要をLLMで生成する
        """
        try:
            with open(instructions_prompt_path, "r", encoding="utf8") as f:
                instructions_prompt = f.read()

            response = completion(
                model=self.aira_config["aira"]["llm"]["model"],
                messages=[{"role": "user", "content": instructions_prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating repository summary: {e}")
            return None
        
    def save_repository_summary(self, summary, output_dir=".aira", output_file="repository_summary_raw.md"):
        """
        リポジトリ概要をファイルに保存する
        """
        os.makedirs(output_dir, exist_ok=True)  # 出力ディレクトリが存在しない場合は作成
        file_path = os.path.join(output_dir, output_file)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(summary)
            logger.info(f"Saved repository summary to {file_path}")
        except Exception as e:
            logger.error(f"Error saving repository summary: {e}")