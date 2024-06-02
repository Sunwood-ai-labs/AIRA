# aira/aira.py
from loguru import logger
from .repository_manager import RepositoryManager
from .commit_manager import CommitManager
from gaiah.gaiah import Gaiah
from gaiah.cli import load_config
from harmon_ai.harmon_ai import HarmonAI
import pprint

class Aira:
    def __init__(self, config_path=".aira/config.yml"):
        logger.debug(f"aira config_path : {config_path}")
        self.config = load_config(config_path)
        gaiah_config_path = self.config["aira"]["gaiah"]["config_path"]
        logger.debug(f"gaiah_config_path : {gaiah_config_path}")
        self.gaiah_config = load_config(gaiah_config_path)
        
        self.repo_manager = RepositoryManager(self.gaiah_config)
        self.commit_manager = CommitManager(self.config)

    def run(self):
        logger.info("Gaiah run : {}".format(self.config["aira"]["gaiah"]["run"]))
        if self.config["aira"]["gaiah"]["run"]:
            logger.info("Gaiah section starting...")
            
            if not self.repo_manager.is_initialized():
                logger.info("Initializing repository...")
                self.repo_manager.init()
                self.gaiah_config["gaiah"] = self.merge_configs(self.gaiah_config["gaiah"], self.gaiah_config["init"])
            else:
                logger.info("Develop repository...")
                self.gaiah_config["gaiah"] = self.merge_configs(self.gaiah_config["gaiah"], self.gaiah_config["dev"])
            
            pprint.pprint(self.gaiah_config)
            gaiah = Gaiah(self.gaiah_config)
            gaiah.run()  # Gaiahの実行

        logger.info("Harmon AI run : {}".format(self.config["aira"]["harmon_ai"]["run"]))
        if self.config["aira"]["harmon_ai"]["run"]:
            logger.info("HarmonAI section starting...")
            config_path = self.config["aira"]["harmon_ai"]["config_path"]
            logger.info(f"config_path is {config_path}")
            harmon_ai = HarmonAI(config_path=config_path)
            harmon_ai.run()  # HarmonAIの実行

    def merge_configs(self, base_config, override_config):
        merged_config = base_config.copy()
        for key, value in override_config.items():
            if isinstance(value, dict):
                merged_config[key] = self.merge_configs(merged_config.get(key, {}), value)
            else:
                merged_config[key] = value
        return merged_config