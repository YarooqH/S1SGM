import os
import shutil
from datetime import datetime

class SaveManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def create_backup(self):
        """Create a local backup of save files"""
        if not os.path.exists(self.config_manager.config["save_dir"]):
            raise Exception(f"Save directory not found: {self.config_manager.config['save_dir']}")
        
        backup_dir = os.path.join(
            self.config_manager.config_dir, 
            "backups",
            f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if not os.path.exists(os.path.dirname(backup_dir)):
            os.makedirs(os.path.dirname(backup_dir))
        
        shutil.copytree(self.config_manager.config["save_dir"], backup_dir)
        return backup_dir

    def get_save_games(self, user_folder):
        """Get list of save games for a specific user folder"""
        user_dir = os.path.join(self.config_manager.config["save_dir"], user_folder)
        if not os.path.exists(user_dir):
            return []
        
        return [f for f in os.listdir(user_dir) 
                if os.path.isdir(os.path.join(user_dir, f))] 