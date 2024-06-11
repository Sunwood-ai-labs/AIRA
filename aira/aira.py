# aira/aira.py
from loguru import logger
from .repository_manager import RepositoryManager
from .commit_manager import CommitManager
from gaiah.gaiah import Gaiah
from gaiah.cli import load_config
from harmon_ai.harmon_ai import HarmonAI
import pprint

from litellm import completion
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

class Aira:
    def __init__(self, config_path=".aira/config.yml"):
        logger.debug(f"aira config_path : {config_path}")
        self.aira_config = load_config(config_path)
        self.gaiah_config = {"gaiah" : self.aira_config["aira"]["gaiah"]}
        
        self.repo_manager = RepositoryManager(self.gaiah_config, self.aira_config)
        self.commit_manager = CommitManager(self.aira_config)

    def make_repo(self):
        logger.info("Gaiah run : {}".format(self.aira_config["aira"]["gaiah"]["run"]))
        if self.aira_config["aira"]["gaiah"]["run"]:
            logger.info("Gaiah section starting...")
            
            if not self.repo_manager.is_initialized():
                logger.info("Initializing repository...")
                self.repo_manager.init()
                self.gaiah_config["gaiah"] = self.merge_configs(self.gaiah_config["gaiah"], self.gaiah_config["gaiah"]["init"])
                
                gaiah = Gaiah(self.gaiah_config)
                gaiah.run()  # Gaiahの実行
            else:
                logger.info("Develop repository...")
                self.gaiah_config["gaiah"] = self.merge_configs(self.gaiah_config["gaiah"], self.gaiah_config["gaiah"]["dev"])
            
        logger.info("Harmon AI run : {}".format(self.aira_config["aira"]["harmon_ai"]["run"]))
        if self.aira_config["aira"]["harmon_ai"]["run"]:
            logger.info("HarmonAI section starting...")
                       
            output_dir = self.aira_config["aira"]["harmon_ai"]["development"]["output_dir"]
            # output_dir = self.aira_config.get("repository_summary_output_dir", ".aira")
            logger.debug(f"output_dir is [{output_dir}]")
            # リポジトリ概要を生成
            instructions_prompt_path = self.aira_config["aira"]["harmon_ai"]["instructions_prompt"]
            repository_summary = self.repo_manager.generate_repository_summary(
                instructions_prompt_path
            )
            
            # リポジトリ概要を保存
            output_file="repository_summary_raw.md"
            self.repo_manager.save_repository_summary(repository_summary, output_dir, output_file)
            
            repository_summary_raw = os.path.join(output_dir, output_file)
            with open(repository_summary_raw, "r", encoding="utf-8") as f:
                repository_summary =  f.read()

            # # README を生成
            readme_prompt_template_path = r".aira\prompt_readme.md"
            readme = self.generate_readme(
                repository_summary, readme_prompt_template_path
            )
            
            output_file = "sections_template_llm.md"
            self.repo_manager.save_repository_summary(readme, output_dir, output_file)
            
            harmon_ai_config = {"harmon_ai" : self.aira_config["aira"]["harmon_ai"]}
            harmon_ai_config["harmon_ai"]["product"]["sections_content_file"] = output_file
            harmon_ai = HarmonAI(config=harmon_ai_config)
            harmon_ai.run()  # HarmonAIの実行
    
    def run(self):
        logger.info("Gaiah run : {}".format(self.aira_config["aira"]["gaiah"]["run"]))
        if self.aira_config["aira"]["gaiah"]["run"]:
            logger.info("Gaiah section starting...")
            
            if self.repo_manager.is_initialized():
                logger.info("Develop repository...")
                self.gaiah_config["gaiah"] = self.merge_configs(self.gaiah_config["gaiah"], self.gaiah_config["gaiah"]["dev"])
                gaiah = Gaiah(self.gaiah_config)
                gaiah.run()  # Gaiahの実行

    def co_and_merge_branches(self):
        if self.aira_config["aira"]["gaiah"]["run"]:
            logger.info("Gaiah section starting...")
            
            if self.repo_manager.is_initialized():
                logger.info("Develop repository...")
                self.gaiah_config["gaiah"] = self.merge_configs(self.gaiah_config["gaiah"], self.gaiah_config["gaiah"]["dev"])
                gaiah = Gaiah(self.gaiah_config)
                gaiah.checkout_and_merge_branches()  # Gaiahの実行
                gaiah.push()  # Gaiahの実行
    
    def merge_configs(self, base_config, override_config):
        merged_config = base_config.copy()
        for key, value in override_config.items():
            if isinstance(value, dict):
                merged_config[key] = self.merge_configs(merged_config.get(key, {}), value)
            else:
                merged_config[key] = value
        return merged_config
    
    
    def generate_readme(self, repository_summary, prompt_template_path=None):
        """
        リポジトリの概要とテンプレートからREADMEを生成する
        """
        try:
            sections_content_path = r".harmon_ai\sections_template.md"
            with open(sections_content_path, "r", encoding="utf-8") as f:
                template = f.read()

            # プロンプトテンプレートファイルの読み込み
            if prompt_template_path:
                try:
                    with open(prompt_template_path, "r", encoding="utf-8") as f:
                        prompt_template = f.read()
                except FileNotFoundError:
                    logger.warning(f"Prompt template file not found: {prompt_template_path}. Using default template.")
                    prompt_template = "下記のテンプレートに従ってリポジトリの概要からREADMEを作成して\n\n# テンプレート\n\n[テンプレート]\n\n# 概要\n\n[概要]"
            else:
                prompt_template = "下記のテンプレートに従ってリポジトリの概要からREADMEを作成して\n\n# テンプレート\n\n[テンプレート]\n\n# 概要\n\n[概要]"

            prompt = prompt_template.replace("[readme_template]", template).replace("[readme_abst]", repository_summary)

            response = completion(
                model=self.aira_config["aira"]["llm"]["model"],
                messages=[{"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating README: {e}")
            return None